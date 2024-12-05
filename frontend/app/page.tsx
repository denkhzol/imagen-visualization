// pages.tsx
'use client';
import React, { useState, useEffect, useRef } from 'react';
import './globals.css';
import dynamic from 'next/dynamic';
import Modal from 'react-modal';
import { useSelector, useDispatch } from 'react-redux';
import { RootState, AppDispatch } from './store';
import * as d3 from 'd3';
import Plotly from 'plotly.js';
import { fetchDataThunk, fetchFilesThunk, fetchConfigThunk, saveConfigThunk, deleteFileThunk, uploadFileThunk} from './slice';

export const useAppDispatch: () => AppDispatch = useDispatch;

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

//plot types
type GraphType = 'scatter' | 'individualVelocities' | 'bar' | 'proximity' | 'stateplot' | 'averageVelocities' | 'heatmap' | 'stateTimeline' | 'velocity' | 'avgvelocity' | 'proximityGraph';

interface PlotCardProps {
  graphType: GraphType;
  onRemove: () => void;
  onEnlarge: (data: any[]) => void;
}

//plot data rendering
const PlotCard: React.FC<PlotCardProps> = ({ graphType, onRemove, onEnlarge }) => {
  let data: any[];
  switch (graphType) {
    case 'scatter':
      data = useSelector((state: RootState) => state.mySliceName.staticTrajectories);
      break;
    case 'individualVelocities':
      data = useSelector((state: RootState) => state.mySliceName.individualVelocities);
      break;
    case 'bar':
      data = [useSelector((state: RootState) => state.mySliceName.distanceBar)]
      break;
    case 'proximity':
      data = [useSelector((state: RootState) => state.mySliceName.proximityBar)];
      break;
    case 'stateplot':
      data = useSelector((state: RootState) => state.mySliceName.statePlot);
      break;
    case 'averageVelocities':
      data = [useSelector((state: RootState) => state.mySliceName.averageVelocities)];
      break;
    case 'heatmap':
      data = [useSelector((state: RootState) => state.mySliceName.heatMap)];
      break;
    case 'stateTimeline':
      let timelineData = useSelector((state: RootState) => state.mySliceName.stateTimeline);
      const traces = [...timelineData.data_moving, ...timelineData.data_sitting];
      const updatedTraces = traces.map(trace => ({
        ...trace,
        line: trace.y[0] === "sitting" ? { width: 200, color: 'green' } : { width: 200, color: 'orange' },
      }));
      data = updatedTraces;
      break;
    case 'velocity':
      data = [useSelector((state: RootState) => state.mySliceName.velocity.lines), useSelector((state: RootState) => state.mySliceName.velocity.markers)];
      break;
    case 'avgvelocity':
      data = [useSelector((state: RootState) => state.mySliceName.avgVelocity.lines), useSelector((state: RootState) => state.mySliceName.avgVelocity.markers), useSelector((state: RootState) => state.mySliceName.avgVelocity.points)];
      break;
    case 'proximityGraph':
      const nodes = useSelector((state: RootState) => state.mySliceName.networkGraph.nodes);
      const edges = useSelector((state: RootState) => state.mySliceName.networkGraph.edges);
      const colorScale: d3.ScaleLinear<string, string> = d3.scaleLinear<string>().domain([1, 2, 3]).range(["green", "red", "blue"]);4
      const edgeTraces = edges.map(edge => {
        const sourceNode = nodes.find(node => node.id === edge.source)!;
        const targetNode = nodes.find(node => node.id === edge.target)!;
  
        return {
          x: [sourceNode.x, targetNode.x, null], 
          y: [sourceNode.y, targetNode.y, null], 
          mode: 'lines',
          line: {
            color: colorScale(edge.weight),
            width: edge.weight * 2 
          },
          hoverinfo: 'none'
        };
      });

      const nodeTrace = {
        x: nodes.map(node => node.x),
        y: nodes.map(node => node.y),
        text: nodes.map(node => node.label),
        mode: 'markers+text',
        textposition: 'top center',
        marker: {
          //size: nodes.map(node => node.size),
          color: nodes.map(node => node.color),
        },
        hoverinfo: 'text'
      };
      data = [...edgeTraces, nodeTrace];
      break;
    default:
      data = [];
  }
  //layout rendering
  let layout: any;
  if(graphType == "stateTimeline")
  {
    layout =  {
      xaxis: { title: "frames", range: [0, 100] },
      yaxis: { title: "States", type: "category" },
      showlegend: false,
      width: 1130, height: 320
    }
  }
  else if(graphType == "proximityGraph")
  {
    layout = {
      xaxis: { visible: false },
      yaxis: { visible: false },
      showlegend: false,
      margin: { t: 50, b: 0, l: 0, r: 0 },
      width: 1130, 
      height: 320
    };
  } else{
    layout = { visible: true, width: 300, height: 300, barmode: graphType.includes("stateplot") ? 'stack' : 'group' };
  }
  const clonnedLayout = JSON.parse(JSON.stringify(layout));
  const clonnedData = JSON.parse(JSON.stringify(data));
    

  return (
    <div className={graphType == "stateTimeline" ||  graphType == "proximityGraph" ? "plot-card wide-card" : "plot-card"}>
      <div className="plot-title">{graphType.charAt(0).toUpperCase() + graphType.slice(1) + " Graph"}</div>
      <button className="close-btn" onClick={onRemove}>&times;</button>
      {graphType == "stateTimeline" ||  graphType == "proximityGraph"  ? <></> : <button className="enlarge-btn" onClick={() => onEnlarge(data)}>🔍</button>}
      <div style={{ height: '300px' }}>
        {/* ploting the graph using plotly */}
        <Plot data={clonnedData} layout={clonnedLayout} />
      </div>
    </div>
  );
};

interface EnlargedGraphModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  data: any[];
  graphType: string;
}

//popup component
const EnlargedGraphModal: React.FC<EnlargedGraphModalProps> = ({ isOpen, onRequestClose, data, graphType }) => {
  
    const layout: Partial<Plotly.Layout> = {
      width: 500,
      height: 500,
      barmode: graphType.includes('stateplot') ? 'stack' : 'group',
    };

   const clonnedLayout = JSON.parse(JSON.stringify(layout));
   const clonnedData = JSON.parse(JSON.stringify(data));

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      ariaHideApp={false}
      className="modal-content"
      style={{ content: { padding: '20px' } }} // Optionally adjust modal content style
    >
      <div className="modal-header">
        <h5 className="modal-title">Enlarged Graph</h5>
        <button type="button" className="close" onClick={onRequestClose}>
          &times;
        </button>
      </div>
      <div className="modal-body" style={{ height: '500px' }}>
        {/* ploting the graph using plotly */}
        <Plot data={clonnedData} layout={clonnedLayout}/>
      </div>
    </Modal>
  );
};

const Page: React.FC = () => {
  const dispatch = useAppDispatch();
 
   // Access Redux state directly using `useSelector`
   const stateRadius = useSelector((state: RootState) => state.mySliceName.radius);
   const stateSubject = useSelector((state: RootState) => state.mySliceName.subject);
   const stateSelectedFile = useSelector((state: RootState) => state.mySliceName.fileNameSelected);
   const stateSelectedAnimal = useSelector((state: RootState) => state.mySliceName.animal);
   const stateFileOptions = useSelector((state: RootState) => state.mySliceName.fileNames);
 
   // Local state to track the selection
   const [graphs, setGraphs] = useState<GraphType[]>([]);
   const [modalData, setModalData] = useState<any[]>([]);
   const [modalIsOpen, setModalIsOpen] = useState<boolean>(false);
   const [selectedGraph, setSelectedGraph] = useState<string>("");
   const [radius, setRadius] = useState<string>(stateRadius);
   const [subject, setSubject] = useState<string>(stateSubject);
   const [selectedFile, setSelectedFile] = useState<string>(stateSelectedFile);
   const [animal, setAnimal] = useState<string>(stateSelectedAnimal);
   const [deleteFile, setdeleteFile] = useState<string>('');
   const [fileOptions, setFileOptions] = useState<string[]>(stateFileOptions);

   useEffect(() => {
    setFileOptions(stateFileOptions);
  }, [stateFileOptions]);

    useEffect(() => {
      setRadius(stateRadius);
    }, [stateRadius]);
  
    useEffect(() => {
      setSubject(stateSubject);
    }, [stateSubject]);
  
    useEffect(() => {
      setSelectedFile(stateSelectedFile);
    }, [stateSelectedFile]);

    useEffect(() => {
      setAnimal(stateSelectedAnimal);
    }, [stateSelectedAnimal]);

  //fetch data based on configuration
  const fetchDataOnLoad = async () => {
    const resultAction = await dispatch(fetchDataThunk());

    if (fetchDataThunk.fulfilled.match(resultAction)) {
      alert("Data loaded successfully!")
    } else if (fetchDataThunk.rejected.match(resultAction)) {
      alert("Error fetching data!")
    }
  };
  //fetch dowpdown files list
  const fetchFilesOnLoad = async () => {
    const resultAction = await dispatch(fetchFilesThunk());
    if (fetchFilesThunk.fulfilled.match(resultAction)) {
      console.log('Data fetched successfully:', resultAction.payload);
    } else if (fetchFilesThunk.rejected.match(resultAction)) {
      console.error('Error fetching data:', resultAction.payload);
    }
  };
  //fetch config data
  const fetchConfigOnLoad = async () => {
    const resultAction = await dispatch(fetchConfigThunk());

    if (fetchConfigThunk.fulfilled.match(resultAction)) {
      console.log('Data fetched successfully:', resultAction.payload);
    } else if (fetchConfigThunk.rejected.match(resultAction)) {
      console.error('Error fetching data:', resultAction.payload);
    }
  };


  const handleAddGraph = (graphType: any) => {
    setGraphs([...graphs, graphType]);
    setSelectedGraph(graphType);
  };

  const handleRemoveGraph = (index: any) => {
    setGraphs(graphs.filter((_: any, i: any) => i !== index));
  };

  const handleEnlargeGraph = (data: any) => {
    setModalData(data);
    setModalIsOpen(true);
  };

  const handleCloseModal = () => {
    setModalIsOpen(false);
    setModalData([]);
  };

  const handleChangeRadius = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRadius(event.target.value);
  };

  const handleChangeSubject = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSubject(event.target.value);
  };
  
  const handleFileChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedFile(event.target.value);
  };

  const handleAnimalChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setAnimal(event.target.value);
  };

  const handleDeleteFileChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setdeleteFile(event.target.value);
  };

  //handle delete file by calling delete file thunk
  const handleDelete = async () => {
    if (!deleteFile) {
      alert('Please select a file to delete.');
      return;
    }
    try {
      const resultAction = await dispatch(deleteFileThunk(deleteFile));
  
      if (deleteFileThunk.fulfilled.match(resultAction)) {
        alert('File deleted successfully!');
        setdeleteFile('');
        fetchFilesOnLoad();
      } else if (deleteFileThunk.rejected.match(resultAction)) {
        alert(resultAction.payload || 'Failed to delete the file.');
      }
    } catch (error) {
      console.error('Unexpected error:', error);
      alert('An unexpected error occurred.');
    }
  };

  //handle save configuration by dispatching saveConfigThunk
  const handleSave = async () => {
    const payload = { radius, subject, selectedFile, animal };
    try {
      await dispatch(saveConfigThunk(payload));
      fetchDataOnLoad();
      fetchConfigOnLoad();
      alert('Configuration saved successfully!');
    } catch (error) {
      alert('Error occurred during save.');
    }
  };

  //handle file upload 
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files ? event.target.files[0] : null;
    if (uploadedFile) {
    await dispatch(uploadFileThunk(uploadedFile));
    await fetchFilesOnLoad();
     alert('File uploaded successfully!');
    }
  };

  
  useEffect(() => {
    debugger;
    //trigger data fetch on load
    fetchDataOnLoad();
    fetchFilesOnLoad();
    fetchConfigOnLoad();
  }, []);

  return (
    <div>
      <div className="sidebar">
        <div className="container filter-bar">
          <div className="row">
            <div className="col-md-12">
              <h3>Configuration</h3>
            </div>
            <div className="col-md-12">
              <select className="form-control" value={selectedFile} onChange={handleFileChange} id="dropdown1">
                <option value='' disabled>Select file</option>
                {fileOptions.map((file: string, index: number) => (
                  <option key={index} value={file}>
                    {file}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-12">
              <select className="form-control" value={animal} onChange={handleAnimalChange} id="dropdown6">
                <option value='' disabled>Select Animal</option>
                <option value='pig'>pig</option>
                <option value='chicken'>chicken</option>
              </select>
            </div>
            <div className="col-md-12">
              <input className="form-control" type="text" name="textbox" placeholder="Radius" value={radius} onChange={handleChangeRadius} />
            </div>
            <div className="col-md-12">
              <input className="form-control" type="text" name="textbox" placeholder="Subject" value={subject} onChange={handleChangeSubject}/>
            </div>
            <div className="col-md-12">
              <button type="button" onClick={handleSave} className="upload-label">Save</button>
            </div>
          </div>
          <div className="row addmargin20">
            <h3>Graph Rendering</h3>
            <div className="col-md-12">
              <select className="form-control" id="dropdown3" defaultValue={"DEFAULT"} onChange={(e) => handleAddGraph(e.target.value)}>
                <option style={{ display: 'none' }} value="DEFAULT" disabled >Select Graph Type</option>
                <option value="scatter" >Static Trajectories</option>
                <option value="individualVelocities">Individual Velocities</option>
                <option value="bar">Bar Chart</option>
                <option value="proximity">Proximity Chart</option>
                <option value="stateplot">State Plot</option>
                <option value="averageVelocities">Average Velocities</option>
                <option value="heatmap">Heatmap</option>
                <option value="stateTimeline">State Timeline</option>
                <option value="velocity">Velocity</option>
                <option value="avgvelocity">Average Velocity</option>
                <option value="proximityGraph">Proximity Graph</option>
              </select>
            </div>
          </div>
          <div className="row addmargin20">
            <h3>Upload File</h3>
            <div className="col-md-12">
              <div className="upload-wrapper">
                <label htmlFor="fileUpload" className="upload-label" >Upload TXT File</label>
                <input type="file" className="form-control-file" id="fileUpload" onChange={handleFileUpload} />
              </div>
            </div>
          </div>
          <div className="row addmargin20">
            <h3>Delete File</h3>
            <div className="col-md-12">
            <select className="form-control" value={deleteFile} id="dropdown1" onChange={handleDeleteFileChange}>
                <option value='' disabled>Select file</option>
                {fileOptions.map((file: string, index: number) => (
                  <option key={index} value={file}>
                    {file}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-12">
              <div className="upload-wrapper">
                <button className="upload-label" onClick={handleDelete}>Delete TXT File</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container addmargin">
        <div className="plot-grid addmargin-plotgrid" id="plotGrid">
          {graphs.map((graphType: any, index: any) => (
            <PlotCard
              key={index}
              graphType={graphType}
              onRemove={() => handleRemoveGraph(index)}
              onEnlarge={handleEnlargeGraph}
            />
          ))}
        </div>
      </div>

      {modalData && (
        <EnlargedGraphModal
          isOpen={modalIsOpen}
          onRequestClose={handleCloseModal}
          data={modalData}
          graphType={selectedGraph}
        />
      )}
    </div>
  );
};

export default Page;
