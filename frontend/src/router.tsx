import { createBrowserRouter } from "react-router-dom";

import App from "@/App";
import { ProtectedLayout } from "@/components/ProtectedLayout";
import { Home } from "@/pages/Home";

const NotFound = () => <p style={{ padding: "2rem" }}>Page not found.</p>;
const ConfigError = () => (
  <p style={{ padding: "2rem" }}>
    API key is required but `VITE_APP_API_KEY` is missing. Add it in frontend `.env`.
  </p>
);

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        element: <ProtectedLayout />,
        children: [{ index: true, element: <Home /> }]
      },
      { path: "configuration-error", element: <ConfigError /> }
    ]
  },
  { path: "*", element: <NotFound /> }
]);
