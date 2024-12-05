import { configureStore } from '@reduxjs/toolkit';
import mySlice from './slice';

const store = configureStore({
  reducer: {
    mySliceName: mySlice,
  },
});
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
