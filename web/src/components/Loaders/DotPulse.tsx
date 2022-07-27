import styled, { keyframes } from 'styled-components';

const dotPulse = keyframes`
 0% {
    box-shadow: 9999px 0 0 -5px var(--text-color-light);
  }

  30% {
    box-shadow: 9999px 0 0 2px var(--text-color-light);
  }

  60%,
  100% {
    box-shadow: 9999px 0 0 -5px var(--text-color-light);
  }`;

const dotPulseBefore = keyframes`
  0% {
    box-shadow: 9983px 0 0 -5px var(--text-color-light);
  }

  30% {
    box-shadow: 9983px 0 0 2px var(--text-color-light);
  }

  60%,
  100% {
    box-shadow: 9983px 0 0 -5px var(--text-color-light);
  }
`;

const dotPulseAfter = keyframes`
  0% {
    box-shadow: 10015px 0 0 -5px var(--text-color-light);
  }

  30% {
    box-shadow: 10015px 0 0 2px var(--text-color-light);
  }

  60%,
  100% {
    box-shadow: 10015px 0 0 -5px var(--text-color-light);
  }
`;

const Pulse = styled.div`
  position: relative;
  left: -9999px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background-color: var(--text-color-light);
  color: var(--text-color-light);
  box-shadow: 9999px 0 0 -5px var(--text-color-light);
  animation: ${dotPulse} 1.5s infinite linear;
  animation-delay: 0.25s;

  &::before,
  &::after {
    content: '';
    display: inline-block;
    position: absolute;
    top: 0;
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background-color: var(--text-color-light);
    color: var(--text-color-light);
  }

  &::before {
    box-shadow: 9983px 0 0 -5px var(--text-color-light);
    animation: ${dotPulseBefore} 1.5s infinite linear;
    animation-delay: 0s;
  }

  &::after {
    box-shadow: 10015px 0 0 -5px var(--text-color-light);
    animation: ${dotPulseAfter} 1.5s infinite linear;
    animation-delay: 0.5s;
  }
`;

function DotPulse() {
  return <Pulse />;
}

export default DotPulse;
