import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import {
  Container,
  Paper,
  Typography,
  Button,
  CircularProgress,
  Snackbar,
  AppBar,
  Toolbar,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { Settings } from '@material-ui/icons';
import Editor from "@monaco-editor/react";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import axios from 'axios';
import {
  setSql,
  setOptimizer,
  clearError,
  clearResult,
  activateOptimizer,
  optimizeSql,
  setError
} from './store/sqlSlice';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
  },
  title: {
    flexGrow: 1,
  },
  container: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  editorContainer: {
    marginBottom: theme.spacing(2),
    border: '1px solid #ddd',
    borderRadius: theme.shape.borderRadius,
    overflow: 'hidden',
  },
  buttonContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing(2),
  },
  optimizerSelect: {
    minWidth: 200,
  },
  resultContainer: {
    marginTop: theme.spacing(3),
  },
  explanation: {
    marginTop: theme.spacing(2),
    padding: theme.spacing(2),
    backgroundColor: '#f8f9fa',
    borderRadius: theme.shape.borderRadius,
  },
  issues: {
    marginTop: theme.spacing(2),
    '& li': {
      marginBottom: theme.spacing(1),
    },
  },
}));

function App() {
  const classes = useStyles();
  const dispatch = useDispatch();
  const {
    sql,
    optimizer,
    optimizers,
    result,
    loading,
    error
  } = useSelector(state => state.sql);

  const handleOptimize = async () => {
    if (!sql.trim()) {
      dispatch(setError('Please enter SQL query'));
      return;
    }

    await dispatch(activateOptimizer(optimizer));
    await dispatch(optimizeSql({
      sql,
      prompt: 'Optimize this SQL query for better performance',
      context: {}
    }));
  };

  const handleEditorChange = (value) => {
    dispatch(setSql(value));
  };

  const handleOptimizerChange = (event) => {
    dispatch(setOptimizer(event.target.value));
  };

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            SQL Optimizer
          </Typography>
          <FormControl className={classes.optimizerSelect}>
            <InputLabel>Optimizer</InputLabel>
            <Select
              value={optimizer}
              onChange={handleOptimizerChange}
            >
              {optimizers.map((opt) => (
                <MenuItem key={opt.id} value={opt.id}>
                  {opt.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <IconButton color="inherit">
            <Settings />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container className={classes.container}>
        <Paper className={classes.paper}>
          <Typography variant="h6" gutterBottom>
            Input SQL Query
          </Typography>
          <div className={classes.editorContainer}>
            <Editor
              height="200px"
              defaultLanguage="sql"
              value={sql}
              onChange={handleEditorChange}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
              }}
            />
          </div>
          <div className={classes.buttonContainer}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleOptimize}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Optimize SQL'}
            </Button>
          </div>
        </Paper>

        {result && (
          <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>
              Optimized SQL
            </Typography>
            <div className={classes.editorContainer}>
              <SyntaxHighlighter
                language="sql"
                style={materialDark}
                customStyle={{ margin: 0, padding: '16px' }}
              >
                {result.optimized_sql}
              </SyntaxHighlighter>
            </div>

            <div className={classes.explanation}>
              <Typography variant="h6" gutterBottom>
                Explanation
              </Typography>
              <Typography variant="body1">
                {result.explanation}
              </Typography>
            </div>

            {result.issues.length > 0 && (
              <div className={classes.issues}>
                <Typography variant="h6" gutterBottom>
                  Identified Issues
                </Typography>
                <ul>
                  {result.issues.map((issue, index) => (
                    <li key={index}>
                      <Typography variant="body1">{issue}</Typography>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </Paper>
        )}
      </Container>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => dispatch(clearError())}
      >
        <Alert onClose={() => dispatch(clearError())} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </div>
  );
}

export default App;
