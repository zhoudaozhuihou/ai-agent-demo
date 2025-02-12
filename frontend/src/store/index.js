import { configureStore } from '@reduxjs/toolkit';
import sqlReducer from './sqlSlice';

export const store = configureStore({
  reducer: {
    sql: sqlReducer,
  },
});
