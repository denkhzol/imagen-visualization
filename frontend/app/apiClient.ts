import axios from 'axios';
// Create an Axios instance
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/', 
  timeout: 10000,                      
  headers: {
    'Content-Type': 'application/json',
  },
});

//fetch data from backend API Call
export const fetchData = async () => {
  try {
    const response = await apiClient.get('/data');
    return response.data;
  } catch (error) {
    console.error('Error while fetching data:', error);
    throw error;
  }
};

//fetch Files from backend API Call
export const fetchFiles = async () => {
  try {
    const response = await apiClient.get('/list_files');
    return response.data;
  } catch (error) {
    console.error('Error while fetching data:', error);
    throw error;
  }
};

//fetch Configuration from backend API Call
export const fetchConfig = async () => {
  try {
    const response = await apiClient.get('/config_data');
    return response.data;
  } catch (error) {
    console.error('Error while fetching data:', error);
    throw error;
  }
};

//Save Configuration API Call
export const saveConfig = async (payload: Record<string, any>) => {
  try {
    const response = await apiClient.put('/update_config', payload);
    return response.data;
  } catch (error) {
    console.error('Error while saving data:', error);
    throw error;
  }
};

//Delete File API Call
export const deleteFile = async (fileName: string) => {
  try {
    const formData = new FormData();
    formData.append('file_name', fileName);
    const response = await apiClient.delete('/delete_file', {
      data: formData,
    });
    return response.data;
  } catch (error: any) {
    console.error('Error deleting file:', error);
    throw error;
  }
};

//Upload File API Call
export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await apiClient.post('/upload_file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};

export default apiClient;
