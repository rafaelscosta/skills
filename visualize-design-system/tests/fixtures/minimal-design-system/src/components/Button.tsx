import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

export const buttonVariants = cva("button", {
  variants: {
    variant: {
      primary: "button-primary",
      secondary: "button-secondary",
      ghost: "button-ghost",
      destructive: "button-destructive"
    },
    size: {
      sm: "button-sm",
      md: "button-md",
      lg: "button-lg"
    }
  },
  defaultVariants: {
    variant: "primary",
    size: "md"
  }
});

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

export function Button({ loading, disabled, children, ...props }: ButtonProps) {
  return (
    <button aria-busy={loading || undefined} disabled={disabled || loading} {...props}>
      {children}
    </button>
  );
}
