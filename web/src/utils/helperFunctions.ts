import { FieldErrors } from 'react-hook-form';

type FormErrors = FieldErrors<{ [key: string]: unknown }>;

function checkObjLength(obj: object) {
  return Object.keys(obj).length;
}

function formHasValidationErrors(errors: FormErrors) {
  return checkObjLength(errors) > 0;
}

export { formHasValidationErrors };
