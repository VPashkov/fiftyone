/**
 * @generated SignedSource<<6d9c48677e1823cf4c4b456e45f6f249>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type MediaType = "image" | "video" | "%future added value";
export type DatasetQuery$variables = {
  name: string;
  view?: Array | null;
};
export type DatasetQuery$data = {
  readonly dataset: {
    readonly id: string;
    readonly name: string;
    readonly mediaType: MediaType | null;
    readonly sampleFields: ReadonlyArray<{
      readonly ftype: string;
      readonly subfield: string | null;
      readonly embeddedDocType: string | null;
      readonly path: string;
      readonly dbField: string | null;
    }>;
    readonly frameFields: ReadonlyArray<{
      readonly ftype: string;
      readonly subfield: string | null;
      readonly embeddedDocType: string | null;
      readonly path: string;
      readonly dbField: string | null;
    }>;
    readonly appSidebarGroups: ReadonlyArray<{
      readonly name: string;
      readonly paths: ReadonlyArray<string>;
    }> | null;
    readonly maskTargets: ReadonlyArray<{
      readonly name: string;
      readonly targets: ReadonlyArray<{
        readonly target: number;
        readonly value: string;
      }>;
    }>;
    readonly defaultMaskTargets: ReadonlyArray<{
      readonly target: number;
      readonly value: string;
    }> | null;
    readonly evaluations: ReadonlyArray<{
      readonly key: string;
      readonly version: string;
      readonly timestamp: string;
      readonly viewStages: ReadonlyArray<string>;
      readonly config: {
        readonly cls: string;
        readonly predField: string;
        readonly gtField: string;
      };
    }>;
    readonly brainMethods: ReadonlyArray<{
      readonly key: string;
      readonly version: string;
      readonly timestamp: string;
      readonly viewStages: ReadonlyArray<string>;
      readonly config: {
        readonly cls: string;
        readonly embeddingsField: string | null;
        readonly method: string;
        readonly patchesField: string | null;
      };
    }>;
    readonly lastLoadedAt: string;
    readonly createdAt: string;
    readonly version: string;
  } | null;
};
export type DatasetQuery = {
  variables: DatasetQuery$variables;
  response: DatasetQuery$data;
};

const node: ConcreteRequest = (function(){
var v0 = [
  {
    "defaultValue": null,
    "kind": "LocalArgument",
    "name": "name"
  },
  {
    "defaultValue": null,
    "kind": "LocalArgument",
    "name": "view"
  }
],
v1 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "name",
  "storageKey": null
},
v2 = [
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "ftype",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "subfield",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "embeddedDocType",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "path",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "dbField",
    "storageKey": null
  }
],
v3 = [
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "target",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "value",
    "storageKey": null
  }
],
v4 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "key",
  "storageKey": null
},
v5 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "version",
  "storageKey": null
},
v6 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "timestamp",
  "storageKey": null
},
v7 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "viewStages",
  "storageKey": null
},
v8 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "cls",
  "storageKey": null
},
v9 = [
  {
    "alias": null,
    "args": [
      {
        "kind": "Variable",
        "name": "name",
        "variableName": "name"
      },
      {
        "kind": "Variable",
        "name": "view",
        "variableName": "view"
      }
    ],
    "concreteType": "Dataset",
    "kind": "LinkedField",
    "name": "dataset",
    "plural": false,
    "selections": [
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "id",
        "storageKey": null
      },
      (v1/*: any*/),
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "mediaType",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "SampleField",
        "kind": "LinkedField",
        "name": "sampleFields",
        "plural": true,
        "selections": (v2/*: any*/),
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "SampleField",
        "kind": "LinkedField",
        "name": "frameFields",
        "plural": true,
        "selections": (v2/*: any*/),
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "SidebarGroup",
        "kind": "LinkedField",
        "name": "appSidebarGroups",
        "plural": true,
        "selections": [
          (v1/*: any*/),
          {
            "alias": null,
            "args": null,
            "kind": "ScalarField",
            "name": "paths",
            "storageKey": null
          }
        ],
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "NamedTargets",
        "kind": "LinkedField",
        "name": "maskTargets",
        "plural": true,
        "selections": [
          (v1/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "Target",
            "kind": "LinkedField",
            "name": "targets",
            "plural": true,
            "selections": (v3/*: any*/),
            "storageKey": null
          }
        ],
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "Target",
        "kind": "LinkedField",
        "name": "defaultMaskTargets",
        "plural": true,
        "selections": (v3/*: any*/),
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "EvaluationRun",
        "kind": "LinkedField",
        "name": "evaluations",
        "plural": true,
        "selections": [
          (v4/*: any*/),
          (v5/*: any*/),
          (v6/*: any*/),
          (v7/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "EvaluationRunConfig",
            "kind": "LinkedField",
            "name": "config",
            "plural": false,
            "selections": [
              (v8/*: any*/),
              {
                "alias": null,
                "args": null,
                "kind": "ScalarField",
                "name": "predField",
                "storageKey": null
              },
              {
                "alias": null,
                "args": null,
                "kind": "ScalarField",
                "name": "gtField",
                "storageKey": null
              }
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "BrainRun",
        "kind": "LinkedField",
        "name": "brainMethods",
        "plural": true,
        "selections": [
          (v4/*: any*/),
          (v5/*: any*/),
          (v6/*: any*/),
          (v7/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "BrainRunConfig",
            "kind": "LinkedField",
            "name": "config",
            "plural": false,
            "selections": [
              (v8/*: any*/),
              {
                "alias": null,
                "args": null,
                "kind": "ScalarField",
                "name": "embeddingsField",
                "storageKey": null
              },
              {
                "alias": null,
                "args": null,
                "kind": "ScalarField",
                "name": "method",
                "storageKey": null
              },
              {
                "alias": null,
                "args": null,
                "kind": "ScalarField",
                "name": "patchesField",
                "storageKey": null
              }
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "lastLoadedAt",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "createdAt",
        "storageKey": null
      },
      (v5/*: any*/)
    ],
    "storageKey": null
  }
];
return {
  "fragment": {
    "argumentDefinitions": (v0/*: any*/),
    "kind": "Fragment",
    "metadata": null,
    "name": "DatasetQuery",
    "selections": (v9/*: any*/),
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": (v0/*: any*/),
    "kind": "Operation",
    "name": "DatasetQuery",
    "selections": (v9/*: any*/)
  },
  "params": {
    "cacheID": "33bb58955b13aadd3c3abc537b89af36",
    "id": null,
    "metadata": {},
    "name": "DatasetQuery",
    "operationKind": "query",
    "text": "query DatasetQuery(\n  $name: String!\n  $view: JSONArray\n) {\n  dataset(name: $name, view: $view) {\n    id\n    name\n    mediaType\n    sampleFields {\n      ftype\n      subfield\n      embeddedDocType\n      path\n      dbField\n    }\n    frameFields {\n      ftype\n      subfield\n      embeddedDocType\n      path\n      dbField\n    }\n    appSidebarGroups {\n      name\n      paths\n    }\n    maskTargets {\n      name\n      targets {\n        target\n        value\n      }\n    }\n    defaultMaskTargets {\n      target\n      value\n    }\n    evaluations {\n      key\n      version\n      timestamp\n      viewStages\n      config {\n        cls\n        predField\n        gtField\n      }\n    }\n    brainMethods {\n      key\n      version\n      timestamp\n      viewStages\n      config {\n        cls\n        embeddingsField\n        method\n        patchesField\n      }\n    }\n    lastLoadedAt\n    createdAt\n    version\n  }\n}\n"
  }
};
})();

(node as any).hash = "671e9861e5a3128117633ab7554973b0";

export default node;
