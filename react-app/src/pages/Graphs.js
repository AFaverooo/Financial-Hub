import React, { useState, useEffect, useRef } from 'react';

import axios from 'axios';
import{ Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Colors
} from 'chart.js'
import { Bar, getElementsAtEvent } from 'react-chartjs-2';
ChartJS.register(
  BarElement,
  CategoryScale,
  Colors,
  LinearScale,
  Tooltip,
  Legend
);

function Graphs({endpoint, endpoint_parameter, loadNext}) {
  const [barChartData, setBarChartData] = useState(null);

  useEffect(() => {
      axios.get(
          'http://127.0.0.1:8000/' + String(endpoint) + '/',
          { params: {
              param: endpoint_parameter
          }}
      )
        .then(response => {
          setBarChartData(response.data);
        })
        .catch(error => {
          console.log(error);
        });
    }, [endpoint]);

  let bar_data = new Array();
  let bar_labels = new Array();
  for (let key in barChartData) {
      bar_labels.push(key);
      bar_data.push(barChartData[key]);
  }

  const options = {
      plugins: {
          colors: {
              forceOverride: true
          },
          legend: {
              labels: {
                  color: "white"
              }
          }
      }
  };
  const data = {
    labels : bar_labels,
    datasets : [{
      label : 'spending',
      data : bar_data,
      borderColor : 'black',
      link: bar_labels
    }]
  }
  const chartRef = useRef();
  const onClick = (event) => {
      if (getElementsAtEvent(chartRef.current, event).length > 0) {
          const datasetIndex = getElementsAtEvent(chartRef.current, event)[0].datasetIndex;
          const dataIndex = getElementsAtEvent(chartRef.current, event)[0].index;
          loadNext({
              'next': data.datasets[datasetIndex].link[dataIndex],
              'current': endpoint
          });
      }
  };

  return (
    <div>
      <Bar
      data = {data}
      options = {options}
      onClick = {onClick}
      ref = {chartRef}></Bar>
    </div>
  );
}

export default Graphs;