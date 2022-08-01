import styled from 'styled-components';
import { FieldError as FormFieldError } from 'react-hook-form';

type FormFieldProps = {
  children: React.ReactNode;
  hasError?: FormFieldError;
};

const Container = styled.form.attrs({ autoComplete: 'off' })`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const FormField = styled.div<FormFieldProps>`
  margin-bottom: 3rem;
  width: 100%;

  label {
    display: block;
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
  }

  input,
  select,
  textarea {
    background-color: var(--input-background-color);
    border-width: 1px;
    border-style: solid;
    border-color: ${({ hasError }) =>
      hasError ? 'var(--error-color)' : 'var(--input-border)'};
    border-radius: 0.4rem;
    font-size: 1.4rem;
    font-family: inherit;
    padding: 1.2rem 2rem;
    width: 100%;

    &:focus {
      border-color: var(--primary-color);
    }

    &:disabled {
      cursor: not-allowed;
      opacity: 0.8;
    }
  }

  select {
    appearance: none;
    background-image: url('/icons/down-arrow.svg');
    background-repeat: no-repeat;
    background-position: right;
    background-size: 2rem;
    cursor: pointer;
    text-transform: capitalize;
    background-position-x: '98%';
  }

  textarea {
    min-height: 10rem;
  }
`;

const Button = styled.div`
  max-width: 20rem;
  margin-top: 4rem;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 2rem;
`;

const FooterCaption = styled.div`
  margin-top: 10rem;
`;

const FieldError = styled.p.attrs({ role: 'alert' })`
  color: var(--error-color);
  font-size: 1.2rem;
  font-weight: 500;
  margin-top: 0.6rem;
  text-align: left;
`;

const Field: React.FC<FormFieldProps> = (props) => {
  const { hasError } = props;

  return (
    <FormField hasError={hasError}>
      {props.children}
      {hasError && <FieldError>{hasError.message}</FieldError>}
    </FormField>
  );
};

export { Button, Container, Field, FooterCaption, Grid };
