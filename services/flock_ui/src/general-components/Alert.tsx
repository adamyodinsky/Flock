import React, { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const Alert = ({ children }: Props) => {
  if (React.Children.count(children) === 0) return null;
  return <div className="alert alert-danger">{children}</div>;
};

export default Alert;
