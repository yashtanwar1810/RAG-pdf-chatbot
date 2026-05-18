import { Navigate, Outlet } from "react-router-dom";

import { env } from "@/lib/env";

export const ProtectedLayout = () => {
  if (env.requireApiKey && !env.appApiKey) {
    return <Navigate replace to="/configuration-error" />;
  }
  return <Outlet />;
};
