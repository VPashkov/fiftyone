import { Lookers } from "@fiftyone/state";
import React, { useContext } from "react";

export type GroupContext = {
  lookerRefCallback: (looker: Lookers) => void;
};

const defaultOptions: GroupContext = {
  lookerRefCallback: () => {},
};

export const groupContext = React.createContext<GroupContext>(defaultOptions);

export const useGroupContext = () => useContext(groupContext);

interface GroupContextProviderProps {
  children: React.ReactNode;
  lookerRefCallback: (looker: Lookers) => void;
}

export const GroupContextProvider = ({
  lookerRefCallback,
  children,
}: GroupContextProviderProps) => {
  return (
    <groupContext.Provider
      value={{
        lookerRefCallback,
      }}
    >
      {children}
    </groupContext.Provider>
  );
};
