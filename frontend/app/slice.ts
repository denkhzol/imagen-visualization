import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {initialState} from './state'
import { fetchData, fetchFiles, fetchConfig, saveConfig, deleteFile, uploadFile } from './apiClient';
import {Traces} from './state';

// Define an async thunk using Redux Toolkit's createAsyncThunk to fetch data and update the store using slice
export const fetchDataThunk = createAsyncThunk(
  'mySlice/fetchData',// Action name used to identify this thunk
  async (_, { rejectWithValue }) => {
    try {
      // Attempt to fetch data using the fetchData function
      const data = await fetchData();
      return data;
    } catch (error) {
      // Handle errors that occur during the fetch
      if (error instanceof Error && 'response' in error) {
        const axiosError = error as any;
        return rejectWithValue(axiosError.response?.data || axiosError.message);
      }
      return rejectWithValue(
        (error as Error).message || 'An unknown error occurred'
      );
    }
  }
);

// Define an async thunk using Redux Toolkit's createAsyncThunk to fetch Files and update the store using slice
export const fetchFilesThunk = createAsyncThunk(
  'mySlice/fetchFiles',// Action name used to identify this thunk
  async (_, { rejectWithValue }) => {
    try {
      // Attempt to fetch data using the fetchFiles function
      const data = await fetchFiles();
      return data;
    } catch (error) {
      // Handle errors that occur during the fetch
      if (error instanceof Error && 'response' in error) {
        const axiosError = error as any;
        return rejectWithValue(axiosError.response?.data || axiosError.message);
      }
      return rejectWithValue(
        (error as Error).message || 'An unknown error occurred'
      );
    }
  }
);

// Define an async thunk using Redux Toolkit's createAsyncThunk to fetch Configuration and update the store using slice
export const fetchConfigThunk = createAsyncThunk(
  'mySlice/fetchConfig',// Action name used to identify this thunk
  async (_, { rejectWithValue }) => {
    try {
      // Attempt to fetch data using the fetchConfig function
      const data = await fetchConfig();
      return data;
    } catch (error) {
      // Handle errors that occur during the fetch
      if (error instanceof Error && 'response' in error) {
        const axiosError = error as any;
        return rejectWithValue(axiosError.response?.data || axiosError.message);
      }
      return rejectWithValue(
        (error as Error).message || 'An unknown error occurred'
      );
    }
  }
);

// Define an async thunk using Redux Toolkit's createAsyncThunk to save Configuration and update the store using slice
export const saveConfigThunk = createAsyncThunk(
  'mySliceName/saveConfig',// Action name used to identify this thunk
  async (
    payload: { radius: string; subject: string; selectedFile: string },
    thunkAPI
  ) => {
    try {
      // Attempt to save data using the saveConfig function
      const response = await saveConfig(payload);
      return response;
    } catch (error: any) {
       // Handle errors that occur during the save
      console.error('Save API failed:', error);
      const errorMessage = 'Failed to save data';
      return thunkAPI.rejectWithValue(errorMessage);
    }
  }
);

// Define an async thunk using Redux Toolkit's createAsyncThunk to delete file and update the store using slice
export const deleteFileThunk = createAsyncThunk<
  any,
  string,
  { rejectValue: string }
>(
  'mySliceName/deleteFile',// Action name used to identify this thunk
  async (fileName, { rejectWithValue }) => {
    try {
      // Attempt to delete data using the deleteFile function
      const response = await deleteFile(fileName);
      return response;
    } catch (error: any) {
      // Handle errors that occur during the save
      console.error('Error in deleteFileThunk:', error);
      const errorMessage =
        error?.response?.data?.message || 'Failed to delete the file.';
      return rejectWithValue(errorMessage);
    }
  }
);

// Define an async thunk using Redux Toolkit's createAsyncThunk to upload file and update the store using slice
export const uploadFileThunk = createAsyncThunk(
  'file/uploadFile',// Action name used to identify this thunk
  async (file: File, thunkAPI) => {
    try {
      // Attempt to upload data using the uploadFile function
      const response = await uploadFile(file);
      return response; 
    } catch (error) {
      // Handle errors that occur during the save
      return thunkAPI.rejectWithValue('Failed to upload file');
    }
  }
);

// Define the slice
const mySlice = createSlice({
  name: 'mySliceName', // Slice name
  initialState: initialState,
  reducers: {
    setRadius(state, action) {
      state.radius = action.payload;
    },
    setSubject(state, action) {
      state.subject = action.payload;
    },
    setFileNameSelected(state, action) {
      state.fileNameSelected = action.payload;
    },
    setAnimal(state, action) {
      state.animal = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      //each case is linked to one thunk response by the thunk name example: fetchDataThunk
      //fetchDataThunk
      .addCase(fetchDataThunk.pending, (state) => {
        state.status = 'loading';
        state.loading = true;
      })
      .addCase(fetchDataThunk.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.loading = false;
        action.payload.data.forEach((element: any) => {
          switch (element.title) {
            case 'StaticTrajectory':
              state.staticTrajectories = element.data_list;
              break;
            case 'distanceBar':
              state.distanceBar = element;
              break;
            case 'proximityBar':
              state.proximityBar = element.data_list;
              break;
              case 'ProximityHeatmap':
                state.heatMap = element;
                break;
              case 'ProximityGraph':
                state.networkGraph.edges = element.edges;
                state.networkGraph.nodes = element.nodes;
                break;
              case 'VelocityPlot':
                state.averageVelocities = element.AverageVelocities_data;
                state.individualVelocities = element.IndividualVelocities_data;
                //avgvelocity
                state.avgVelocity.lines = element.avgVelocity.data_plot4_line;
                state.avgVelocity.markers = element.avgVelocity.data_plot4_dots;
                state.avgVelocity.points = element.avgVelocity.data_plot4_x;
                //velocity
                state.velocity.lines = element.velocity.data_3rd_line;
                state.velocity.markers = element.velocity.data_3rd_dots;
                break;
              case 'StatePlot':
                const obj:Traces[] = [];
                obj.push(element.data_eating);
                obj.push(element.data_moving);
                obj.push(element.data_sitting);
                state.statePlot = obj;
                break;
              case 'StateTimeLine':
                state.stateTimeline.data_eating = element.data_eating;
                state.stateTimeline.data_moving = element.data_moving;
                state.stateTimeline.data_sitting = element.data_sitting;
                break;
            default:
              state.error = "No data Found";
          }
        });
      })
      .addCase(fetchDataThunk.rejected, (state, action) => {
        state.status = 'failed';
        state.loading = false;
        state.error = 'An unknown error occurred';
      })
      //fetchFilesThunk
      .addCase(fetchFilesThunk.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchFilesThunk.fulfilled, (state, action) => {
        state.fileNames = action.payload;

      })
      .addCase(fetchFilesThunk.rejected, (state) => {
        state.status = 'failed';
        state.error = 'An unknown error occurred';
      })
      //fetchConfigThunk
      .addCase(fetchConfigThunk.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchConfigThunk.fulfilled, (state, action) => {
        state.fileNameSelected = action.payload.selectedFile;
        state.radius = action.payload.radius;
        state.subject = action.payload.subject;
        state.animal = action.payload.animal;
      })
      .addCase(fetchConfigThunk.rejected, (state) => {
        state.status = 'failed';
        state.error = 'An unknown error occurred';
      })
      //saveConfigThunk
      .addCase(saveConfigThunk.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(saveConfigThunk.fulfilled, (state, action) => {
        state.status = 'succeeded';
      })
      .addCase(saveConfigThunk.rejected, (state, action) => {
        state.status = 'failed';
      })
      //deleteFileThunk
      .addCase(deleteFileThunk.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(deleteFileThunk.fulfilled, (state, action) => {
        state.status = 'succeeded';
      })
      .addCase(deleteFileThunk.rejected, (state, action) => {
        state.status = 'failed';
        state.error = 'An unknown error occurred';
      })
      //uploadFileThunk
      .addCase(uploadFileThunk.pending, (state) => {
        state.loading = true;
        state.error = '';
      })
      .addCase(uploadFileThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.success = "file uploaded successfully"
      })
      .addCase(uploadFileThunk.rejected, (state, action) => {
        state.loading = false; 
        state.error = action.payload as string;
      });
  },
});

export default mySlice.reducer;
