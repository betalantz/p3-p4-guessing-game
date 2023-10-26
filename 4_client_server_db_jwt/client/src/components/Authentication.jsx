import { Button, LinearProgress, Snackbar, Alert } from "@mui/material";
import { Formik, Form, Field } from "formik";
import { TextField } from "formik-mui";
import * as yup from "yup";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../providers/authProvider";
import React, { useState } from "react";
import { registerFetch, loginFetch } from "../api";
import StatusDetail from "./StatusDetail";

export default function Authentication() {
  const { setToken, setLoading } = useAuth();
  const navigate = useNavigate();
  const [isSignup, setIsSignup] = useState(false);
  const [isError, setIsError] = useState(false);
  const [message, setMessage] = useState("");

  const formSchema = yup.object().shape({
    name: yup.string().required("Name is required"),
    password: yup
      .string()
      .min(4, "Password must be at least 4 characters")
      .required("Password is required"),
  });

  const handleSubmit = async (values, setSubmitting) => {
    setLoading(true);
    setMessage("");
    setIsError(false);
    if (isSignup) {
      const res = await registerFetch(values);
      if (!res.ok) {
        setIsError(true);
      }
      const message = await res.json();
      setMessage(message);
    } else {
      const res = await loginFetch(values);
      const resJSON = await res.json();
      if (!res.ok) {
        setIsError(true);
        setMessage(resJSON);
      } else {
        await setToken(resJSON);
        setLoading(false)
        navigate("/dashboard");
      }
    }
    setSubmitting(false);
  };

  return (
    <>
      {message ? (
        <StatusDetail
          message={message}
          isError={isError}
          onCloseHandler={() => setMessage("")}
        />
      ) : null}
      <Formik
        initialValues={{
          name: "",
          password: "",
        }}
        validationSchema={formSchema}
        onSubmit={(values, { setSubmitting }) => {
          setSubmitting(true);
          handleSubmit(values, setSubmitting);
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
              {isSignup ? "Register" : "Login"}
            </Button>
          </Form>
        )}
      </Formik>
      {!isSignup ? (
        <p>
          If you don't have an account yet, click{" "}
          <Button onClick={() => setIsSignup(!isSignup)}>Register</Button> to
          sign up.
        </p>
      ) : (
        <p>
          If you don't need to Register, click{" "}
          <Button onClick={() => setIsSignup(!isSignup)}>Login</Button> to log
          in.
        </p>
      )}{" "}
    </>
  );
}
