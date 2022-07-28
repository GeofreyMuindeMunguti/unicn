import React from 'react';
import styled, { css } from 'styled-components';

import DotPulse from 'src/components/Loaders/DotPulse';

type StyleProps = {
  children: React.ReactNode;
  disabled?: boolean;
  color?: string;
  type?: 'submit' | 'button';
  size?: 'small' | 'medium';
};

type ButtonProps = {
  onClick?: (...args: any) => void;
  loading?: boolean;
};

type Props = StyleProps & ButtonProps;

const StyledButton = styled.button<StyleProps>`
  border: 0;
  border-radius: 0.5rem;
  background-color: ${({ color }) => (color ? color : 'var(--primary-color)')};
  color: var(--text-color-light);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  outline: 0;
  min-width: 14rem;
  padding: 1.2rem 2rem;
  font-weight: 500;
  font-size: 1.4rem;
  font-family: var(--font-links);
  text-transform: capitalize;
  width: 100%;

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  &:hover {
    opacity: 0.8;
  }

  ${({ size }) => {
    switch (size) {
      case 'small':
        return css`
          border-radius: 0.3rem;
          min-width: 10rem;
          padding: 0.8rem 1rem;
          font-size: 1.3rem;
        `;
      default:
        return css`
          min-height: 4rem;
        `;
    }
  }}

  ${({ color }) => {
    if (color === 'transparent') {
      return css`
        border: 1px solid var(--primary-color);
        color: var(--primary-color);
      `;
    }
  }}
`;

const Button: React.FC<Props> = (props) => {
  const { disabled = false, loading = false, size, type = 'submit' } = props;
  const buttonDisabled = disabled || loading;

  // handle click
  const handleClick = () => {
    if (props.onClick) props.onClick();
  };

  return (
    <StyledButton
      color={props.color}
      disabled={buttonDisabled}
      onClick={handleClick}
      size={size}
      type={type}
    >
      {loading ? <DotPulse /> : <span>{props.children}</span>}
    </StyledButton>
  );
};

export default Button;
