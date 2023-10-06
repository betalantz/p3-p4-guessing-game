import { Button, LinearProgress } from '@mui/material';
import { Formik, Form, Field } from 'formik';
import { TextField } from 'formik-mui';
import * as yup from 'yup';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../providers/authProvider';
import React, {useState} from 'react'

export default function Authentication() {

    const { token } = useAuth();
    const navigate = useNavigate();
    const { isSignup, setIsSignup } = useState(false);

    const formSchema = yup.object().shape({
        name: yup.string().required('Name is required'),
        password: yup
            .string()
            .min(4, 'Password must be at least 4 characters')
            .required('Password is required'),
    });

    const handleSubmit = (values) => {
        
    }


  return (
    <>
   
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
        {({ submitForm, isSubmitting, errors, touched }) => (
            <Form>
                <Field
                    component={TextField}
                    name="name"
                    type="text"
                    label="Name"
                    variant="outlined"
                    fullWidth
                    error={!!errors.name && touched.name}
                    helperText={errors.name}
                />
                <br />
                <Field
                    component={TextField}
                    name="password"
                    type="password"
                    label="Password"
                    variant="outlined" 
                    fullWidth
                    error={!!errors.password && touched.password}
                    helperText={errors.password}
                />
                {isSubmitting && <LinearProgress />}
                <br />
                <Button
                    variant="contained"
                    color="primary"
                    disabled={isSubmitting}
                    onClick={submitForm}
                    >
                    {isSignup ? 'Register' : 'Login'}
                    </Button>
            </Form>
        )}
    </Formik>
    <p>If you don't have an account yet, click </p>
    </>
  )
}
