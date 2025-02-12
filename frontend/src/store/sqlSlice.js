import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const activateOptimizer = createAsyncThunk(
  'sql/activateOptimizer',
  async (optimizerId) => {
    await axios.post(`${API_BASE_URL}/optimizers/${optimizerId}/activate`);
    return optimizerId;
  }
);

export const optimizeSql = createAsyncThunk(
  'sql/optimize',
  async ({ sql, prompt, context }) => {
    const response = await axios.post(`${API_BASE_URL}/sql/optimize`, {
      sql,
      prompt,
      context: context || {}
    });
    return response.data;
  }
);

export const sqlSlice = createSlice({
  name: 'sql',
  initialState: {
    sql: '',
    optimizer: 'default',
    optimizers: [
      { id: 'default', name: 'Default (OpenAI)' },
      { id: 'copilot', name: 'GitHub Copilot' }
    ],
    result: null,
    loading: false,
    error: null
  },
  reducers: {
    setSql: (state, action) => {
      state.sql = action.payload;
    },
    setOptimizer: (state, action) => {
      state.optimizer = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    clearResult: (state) => {
      state.result = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(activateOptimizer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(activateOptimizer.fulfilled, (state, action) => {
        state.loading = false;
        state.optimizer = action.payload;
      })
      .addCase(activateOptimizer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(optimizeSql.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.result = null;
      })
      .addCase(optimizeSql.fulfilled, (state, action) => {
        state.loading = false;
        state.result = action.payload;
      })
      .addCase(optimizeSql.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export const { setSql, setOptimizer, clearError, clearResult } = sqlSlice.actions;

export default sqlSlice.reducer;
