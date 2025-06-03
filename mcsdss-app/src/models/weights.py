MCSDSS_Application
│
├── Main
│   ├── Initialize()
│   ├── Load_Data(input_source)
│   ├── Process_Data()
│   ├── Define_Criteria()
│   ├── Evaluate_Alternatives()
│   ├── Generate_Results()
│   └── Display_Results()
│
├── Data_Handler
│   ├── Load_Shapefile(filepath)
│   ├── Load_LatLong(lat, long)
│   ├── Preprocess_Data()
│   └── Save_Data(output_format)
│
├── Criteria_Management
│   ├── Define_Criteria(criteria_list)
│   ├── Weight_Criteria(weights)
│   ├── Normalize_Criteria()
│   └── Aggregate_Criteria()
│
├── Decision_Analysis
│   ├── Evaluate_Alternatives(alternatives)
│   ├── Rank_Alternatives()
│   └── Sensitivity_Analysis()
│
└── User_Interface
    ├── Display_Map()
    ├── Input_Parameters()
    ├── Show_Results()
    └── Export_Results()