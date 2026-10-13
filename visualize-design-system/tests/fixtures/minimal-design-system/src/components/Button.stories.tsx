import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta = { component: Button, title: "Components/Button" } satisfies Meta<typeof Button>;
export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = { args: { children: "Continuar", variant: "primary" } };
export const Disabled: Story = { args: { children: "Continuar", disabled: true } };
export const Loading: Story = { args: { children: "Continuar", loading: true } };
