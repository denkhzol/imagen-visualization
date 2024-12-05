

export interface ScatterData {
  x: number[];
  y: number[];
  mode: string;
  type: string;
  name: string;
}

export const initialScatterData: ScatterData = {
  x: [],
  y: [],
  type:'',
  mode: '',
  name:''
};

const initialstateTimeline = {
  data_eating: [],  
  data_moving: [], 
  data_sitting: []
};

export interface Bar {
  x: number[];
  y: number[];
  type: string;
}

export const initialbar: Bar = {
  x: [],
  y: [],
  type:''
};

export interface Traces {
  x: number[];
  y: number[];
  name: string;
  type: string;
}

export const initialTraces: Traces = {
  x: [],
  y: [],
  type:'',
  name: ''
};

const initialvelocity = {
  markers: initialScatterData,
  lines: initialScatterData
};

const initialavgVelocity = {
  markers: initialScatterData,
  lines: initialScatterData,
  points: initialScatterData
};


const initialnetworkGraph = {
  nodes: [],
  edges: []
};

export interface LineStyle {
  width: number,
  color: string,
};

type LineStyleOrNull = LineStyle | null;

export interface LineTraces {
  x: number[];
  y: string[];
  name: string;
  mode: string;
  line: LineStyleOrNull;
}

export interface Heatmap {
  z: number[][];
  type: string;
}

export const initialHeatmap: Heatmap = {
  z: [],
  type:''
};

export interface Nodes {
  id: number;
  x: number;
  y: number;
  label: string;
 // size: number;
  color: string;
}

export interface Edges {
  source: number;
  target: number;
  weight: number;
}

export interface MyState {
  fileNameSelected: string;
  animal: string;
  radius: string;
  subject: string;
  fileNames: string[];
  animalNumbersList: string[];
  staticTrajectories: ScatterData[];
  distanceBar: Bar;
  proximityBar: Bar;
  heatMap: Heatmap;
  statePlot: Traces[];
  individualVelocities: ScatterData[];
  averageVelocities: ScatterData;
  stateTimeline: {
    data_eating: LineTraces[],
    data_moving: LineTraces[],
    data_sitting: LineTraces[]
  };
  velocity: {
    markers: ScatterData,
    lines: ScatterData
  };
  avgVelocity: {
    lines: ScatterData,
    markers: ScatterData,
    points: ScatterData
  }
  networkGraph: {
    nodes: Nodes[],
    edges: Edges[]
  },
  status: string;
  error: string;
  loading: boolean;
  success: string;
}

export const initialState: MyState = {
  fileNameSelected: '',
  animal: '',
  radius: '',
  subject: '',
  fileNames: [],
  animalNumbersList: [],
  staticTrajectories: [],
  distanceBar: initialbar,
  proximityBar: initialbar,
  heatMap: initialHeatmap,
  statePlot: [],
  individualVelocities: [],
  averageVelocities: initialScatterData,
  stateTimeline: initialstateTimeline,
  velocity: initialvelocity,
  avgVelocity: initialavgVelocity,
  networkGraph: initialnetworkGraph,
  status: '',
  error: '',
  loading:false,
  success: ''
};



