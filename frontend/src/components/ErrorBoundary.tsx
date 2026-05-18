import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false };

  public static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  public componentDidCatch(_error: Error, _errorInfo: ErrorInfo): void {
    // Hook for Sentry/Datadog.
  }

  public render(): ReactNode {
    if (this.state.hasError) {
      return <p className="error">Something went wrong. Please refresh.</p>;
    }
    return this.props.children;
  }
}
