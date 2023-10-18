import { Snackbar, Alert } from "@mui/material";

function StatusDetail({ message, isError, onCloseHandler }) {
  console.log();
  return (
    <>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={!!message}
        autoHideDuration={6000}
        onClose={() => onCloseHandler()}
      >
        <Alert
          severity={isError ? "error" : "success"}
          onClose={() => onCloseHandler()}
        >
          {message.message}
        </Alert>
      </Snackbar>
    </>
  );
}

export default StatusDetail;
