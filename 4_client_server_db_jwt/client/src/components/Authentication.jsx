import { Button, LinearProgress } from '@mui/material';
import { Formik, Form, Field } from 'formik';
import { TextField } from 'formik-mui';
import * as yup from 'yup';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../providers/authProvider';
import React from 'react'

export default function Authentication() {

    const { token } = useAuth();
    const navigate = useNavigate();

    const formSchema = yup.object().shape({
        name: yup.string().required('Name is required'),
        password: yup
            .string()
            .min(4, 'Password must be at least 4 characters')
            .required('Password is required'),
    });

    


  return (
    <Formik
        initialValues={{
            name: '',
            password: '',
        }}
        validationSchema={formSchema}
        onSubmit={(values, { setSubmitting }) => {
            setTimeout(() => {
                setSubmitting(false);
                navigate('/');
            }, 500);
        }}
    >
        {({ submitForm, isSubmitting }) => (
            <Form>
                <Field
                    component={TextField}
                    name="name"
                    type="text"
                    label="Name"
                    variant="outlined"
                    fullWidth
                />
                <br />
                <Field
                    component={TextField}
                    name="password"
                    type="password"
                    label="Password"
                    variant="outlined" 
                    fullWidth
                />
                {isSubmitting && <LinearProgress />}
                <br />
                <Button
                    variant="contained"
                    color="primary"
                    disabled={isSubmitting}
                    onClick={submitForm}
                    >
                    Submit
                    </Button>
            </Form>
        )}
    </Formik>
  )
}
