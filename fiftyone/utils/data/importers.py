"""
Dataset importers.

| Copyright 2017-2020, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
# pragma pylint: disable=redefined-builtin
# pragma pylint: disable=unused-wildcard-import
# pragma pylint: disable=wildcard-import
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *
from future.utils import iteritems

# pragma pylint: enable=redefined-builtin
# pragma pylint: enable=unused-wildcard-import
# pragma pylint: enable=wildcard-import

import os

import eta.core.datasets as etads
import eta.core.image as etai
import eta.core.serial as etas
import eta.core.utils as etau

import fiftyone.core.labels as fol
import fiftyone.core.metadata as fom
import fiftyone.core.sample as fos
import fiftyone.core.utils as fou

from .parsers import (
    ImageClassificationSampleParser,
    ImageDetectionSampleParser,
    ImageLabelsSampleParser,
)


def import_samples(dataset, importer, label_field=None, tags=None):
    """Imports the samples from the given :class:`DatasetImporter` into the
    given :class:`fiftyone.core.dataset.Dataset`.

    Args:
        dataset: a :class:`fiftyone.core.dataset.Dataset`
        importer: a :class:`DatasetImporter`
        label_field (None): the name of the field to use for the labels of the
            input samples. This is required if and only if ``importer`` is a
            :class:`LabeledImageDatasetImporter`
        tags (None): an optional list of tags to attach to each sample

    Returns:
        a list of IDs of the samples that were added to the dataset
    """
    if isinstance(importer, UnlabeledImageDatasetImporter):
        return _import_unlabeled_image_dataset(dataset, importer, tags)

    if isinstance(importer, LabeledImageDatasetImporter):
        return _import_labeled_image_dataset(
            dataset, importer, label_field, tags
        )

    raise ValueError("Unsupported importer type %s" % type(importer))


def _import_unlabeled_image_dataset(dataset, importer, tags):
    with fou.ProgressBar() as pb:
        with importer:
            _samples = []
            for image_path, image_metadata in pb(importer):
                filepath = os.path.abspath(os.path.expanduser(image_path))

                _samples.append(
                    fos.Sample(
                        filepath=filepath, metadata=image_metadata, tags=tags,
                    )
                )

            return dataset.add_samples(_samples)


def _import_labeled_image_dataset(dataset, importer, label_field, tags):
    with fou.ProgressBar() as pb:
        with importer:
            _samples = []
            for image_path, image_metadata, label in pb(importer):
                filepath = os.path.abspath(os.path.expanduser(image_path))

                _samples.append(
                    fos.Sample(
                        filepath=filepath,
                        metadata=image_metadata,
                        tags=tags,
                        **{label_field: label},
                    )
                )

            return dataset.add_samples(_samples)


class DatasetImporter(object):
    """Base interface for importing datasets stored on disk into FiftyOne.

    Args:
        dataset_dir: the dataset directory
    """

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *args):
        self.close(*args)

    def __iter__(self):
        return self

    def __len__(self):
        """The total number of samples that will be imported.

        Raises:
            TypeError: if the total number is not known
        """
        raise TypeError(
            "The number of samples in a '%s' is not known a priori"
            % etau.get_class_name(self)
        )

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            subclass-specific information for the sample

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")

    def setup(self):
        """Performs any necessary setup before importing the first sample in
        the dataset.

        This method is called when the importer's context manager interface is
        entered, :function:`DatasetImporter.__enter__`.
        """
        pass

    def close(self, *args):
        """Performs any necessary actions after the last sample has been
        imported.

        This method is called when the importer's context manager interface is
        exited, :function:`DatasetImporter.__exit__`.

        Args:
            *args: the arguments to :func:`DatasetImporter.__exit__`
        """
        pass


class UnlabeledImageDatasetImporter(DatasetImporter):
    """Interface for importing datasets of unlabeled image samples.

    Example Usage::

        import fiftyone as fo

        dataset = fo.Dataset(...)

        importer = UnlabeledImageDatasetImporter(dataset_dir, ...)
        with importer:
            for image_path, image_metadata in importer:
                dataset.add_sample(
                    fo.Sample(filepath=image_path, metadata=image_metadata)
                )

    Args:
        dataset_dir: the dataset directory
    """

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            an ``(image_path, image_metadata)`` tuple, where:
            -   ``image_path`` is the path to the image on disk
            -   ``image_metadata`` is an
                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
                image, or ``None`` if :property:`has_image_metadata` is
                ``False``

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")

    @property
    def has_image_metadata(self):
        """Whether this importer produces
        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
        """
        raise NotImplementedError("subclass must implement has_image_metadata")


class LabeledImageDatasetImporter(DatasetImporter):
    """Interface for importing datasets of labeled image samples.

    Example Usage::

        import fiftyone as fo

        dataset = fo.Dataset(...)
        label_field = ...

        importer = LabeledImageDatasetImporter(dataset_dir, ...)
        with importer:
            for image_path, image_metadata, label in importer:
                dataset.add_sample(
                    fo.Sample(
                        filepath=image_path,
                        metadata=image_metadata,
                        **{label_field: label},
                    )
                )

    Args:
        dataset_dir: the dataset directory
    """

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            an  ``(image_path, image_metadata, label)`` tuple, where:
            -   ``image_path`` is the path to the image on disk
            -   ``image_metadata`` is an
                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
                image, or ``None`` if :property:`has_image_metadata` is
                ``False``
            -   ``label`` is an instance of :property:`label_cls`

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")

    @property
    def has_image_metadata(self):
        """Whether this importer produces
        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
        """
        raise NotImplementedError("subclass must implement has_image_metadata")

    @property
    def label_cls(self):
        """The :class:`fiftyone.core.labels.Label` class returned by this
        importer.
        """
        raise NotImplementedError("subclass must implement label_cls")


class ImageDirectoryImporter(UnlabeledImageDatasetImporter):
    """Importer for a directory of images stored on disk.

    See :class:`fiftyone.types.ImageDirectory` for format details.

    Args:
        dataset_dir: the dataset directory
        recursive (True): whether to recursively traverse subdirectories
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, recursive=True, compute_metadata=False):
        super().__init__(dataset_dir)
        self.recursive = recursive
        self.compute_metadata = compute_metadata
        self._filepaths = None
        self._iter_filepaths = None

    def __iter__(self):
        self._iter_filepaths = iter(self._filepaths)
        return self

    def __len__(self):
        return len(self._filepaths)

    def __next__(self):
        image_path = next(self._iter_filepaths)

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    def setup(self):
        filepaths = etau.list_files(
            self.dataset_dir, abs_paths=True, recursive=self.recursive
        )
        self._filepaths = [p for p in filepaths if etai.is_image_mime_type(p)]


class ImageClassificationDatasetImporter(LabeledImageDatasetImporter):
    """Importer for image classification datasets stored on disk.

    See :class:`fiftyone.types.ImageClassificationDataset` for format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._image_paths_map = None
        self._labels = None
        self._iter_labels = None
        self._num_samples = None

    def __iter__(self):
        self._iter_labels = iter(iteritems(self._labels))
        return self

    def __len__(self):
        return self._num_samples

    def __next__(self):
        uuid, target = next(self._iter_labels)
        image_path = self._image_paths_map[uuid]

        sample = (image_path, target)
        label = self._sample_parser.parse_label(sample)

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.Classification

    def setup(self):
        self._sample_parser = ImageClassificationSampleParser()

        data_dir = os.path.join(self.dataset_dir, "data")
        self._image_paths_map = {
            os.path.splitext(os.path.basename(p))[0]: p
            for p in etau.list_files(data_dir, abs_paths=True)
        }

        labels_path = os.path.join(self.dataset_dir, "labels.json")
        labels = etas.load_json(labels_path)
        self._sample_parser.classes = labels.get("classes", None)
        self._labels = labels.get("labels", {})
        self._num_samples = len(self._labels)


class ImageClassificationDirectoryTreeImporter(LabeledImageDatasetImporter):
    """Importer for an image classification directory tree stored on disk.

    See :class:`fiftyone.types.ImageClassificationDirectoryTree` for format
    details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._samples = None
        self._iter_samples = None

    def __iter__(self):
        self._iter_samples = iter(self._samples)
        return self

    def __len__(self):
        return len(self._samples)

    def __next__(self):
        image_path, label = next(self._iter_samples)

        sample = (image_path, label)
        label = self._sample_parser.parse_label(sample)

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.Classification

    def setup(self):
        self._sample_parser = ImageClassificationSampleParser()

        self._samples = []
        glob_patt = os.path.join(self.dataset_dir, "*", "*")
        for path in etau.get_glob_matches(glob_patt):
            chunks = path.split(os.path.sep)
            if any(s.startswith(".") for s in chunks[-2:]):
                continue

            label = chunks[-2]
            self._samples.append((path, label))


class ImageDetectionDatasetImporter(LabeledImageDatasetImporter):
    """Importer for image detection datasets stored on disk.

    See :class:`fiftyone.types.ImageDetectionDataset` for format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._image_paths_map = None
        self._labels = None
        self._iter_labels = None
        self._num_samples = None

    def __iter__(self):
        self._iter_labels = iter(iteritems(self._labels))
        return self

    def __len__(self):
        return self._num_samples

    def __next__(self):
        uuid, target = next(self._iter_labels)
        image_path = self._image_paths_map[uuid]

        sample = (image_path, target)
        label = self._sample_parser.parse_label(sample)

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.Detections

    def setup(self):
        self._sample_parser = ImageDetectionSampleParser()

        data_dir = os.path.join(self.dataset_dir, "data")
        self._image_paths_map = {
            os.path.splitext(os.path.basename(p))[0]: p
            for p in etau.list_files(data_dir, abs_paths=True)
        }

        labels_path = os.path.join(self.dataset_dir, "labels.json")
        labels = etas.load_json(labels_path)
        self._sample_parser.classes = labels.get("classes", None)
        self._labels = labels.get("labels", {})
        self._num_samples = len(self._labels)


class ImageLabelsDatasetImporter(LabeledImageDatasetImporter):
    """Importer for image labels datasets stored on disk.

    See :class:`fiftyone.types.ImageLabelsDataset` for format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._labeled_dataset = None
        self._iter_labeled_dataset = None

    def __iter__(self):
        self._iter_labeled_dataset = zip(
            self._labeled_dataset.iter_data_paths(),
            self._labeled_dataset.iter_labels(),
        )
        return self

    def __len__(self):
        return len(self._labeled_dataset)

    def __next__(self):
        image_path, image_labels = next(self._iter_labeled_dataset)

        sample = (image_path, image_labels)
        label = self._sample_parser.parse_label(sample)

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.ImageLabels

    def setup(self):
        self._sample_parser = ImageLabelsSampleParser()
        self._labeled_dataset = etads.load_dataset(self.dataset_dir)


def parse_images_dir(dataset_dir, recursive=True):
    """Parses the contents of the given directory of images.

    See :class:`fiftyone.types.ImageDirectory` for format details. In
    particular, note that files with non-image MIME types are omitted.

    Args:
        dataset_dir: the dataset directory
        recursive (True): whether to recursively traverse subdirectories

    Returns:
        a list of image paths
    """
    filepaths = etau.list_files(
        dataset_dir, abs_paths=True, recursive=recursive
    )
    return [p for p in filepaths if etai.is_image_mime_type(p)]


def parse_image_classification_dir_tree(dataset_dir):
    """Parses the contents of the given image classification dataset directory
    tree, which should have the following format::

        <dataset_dir>/
            <classA>/
                <image1>.<ext>
                <image2>.<ext>
                ...
            <classB>/
                <image1>.<ext>
                <image2>.<ext>
                ...

    Args:
        dataset_dir: the dataset directory

    Returns:
        samples: a list of ``(image_path, target)`` pairs
        classes: a list of class label strings
    """
    # Get classes
    classes = sorted(etau.list_subdirs(dataset_dir))
    labels_map_rev = {c: i for i, c in enumerate(classes)}

    # Generate dataset
    glob_patt = os.path.join(dataset_dir, "*", "*")
    samples = []
    for path in etau.get_glob_matches(glob_patt):
        chunks = path.split(os.path.sep)
        if any(s.startswith(".") for s in chunks[-2:]):
            continue

        target = labels_map_rev[chunks[-2]]
        samples.append((path, target))

    return samples, classes
