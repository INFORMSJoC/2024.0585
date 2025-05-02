[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# CacheTest

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[Early Detection of Adverse Drug Reactions in Post-Market Monitoring](https://doi.org/10.1287/ijoc.2024.0585) by L. Duan, W. Zhou, Y. Hu, L. Xu, and M. Liu. 
The snapshot is based on 
[this SHA](https://github.com/tkralphs/JoCTemplate/commit/f7f30c63adbcb0811e5a133e1def696b74f3ba15) 
in the development repository. 

**Important: This code is being developed on an on-going basis at 
https://github.com/lian-duan-hofstra/2024.0585. Please go there if you would like to
get a more recent version or would like support**

## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2024.0585

https://doi.org/10.1287/ijoc.2024.0585.cd

Below is the BibTex for citing this snapshot of the repository.

```
@misc{CacheTest,
  author =        {L. Duan and W. Zhou and Y. Hu and L. Xu and M. Liu},
  publisher =     {INFORMS Journal on Computing},
  title =         {{Early Detection of Adverse Drug Reactions in Post-Market Monitoring}},
  year =          {2025},
  doi =           {10.1287/ijoc.2024.0585.cd},
  url =           {https://github.com/INFORMSJoC/2024.0585},
  note =          {Available for download at https://github.com/INFORMSJoC/2024.0585},
}  
```

## Software Overview

The goal of this software is to identify highly correlated variable pairs by analyzing their contingency tables generated from transaction-type raw data.

## Requirements

- Python 3.8 or above

## Setup Instructions

To replicate our results:

1. Place all files and folders from the `src` directory into your project’s root folder.
2. Also place the `data` folder into the root directory.

Your project root should contain:
- A folder named `api`
- A folder named `data`
- Three Python files


## Running Evaluations

### Real Data Evaluation
Computes the **RDCG score** under various significance levels for real datasets:
```bash
python evaluation_real_data_rdcg.py

### Simulated Data Evaluation
Computes the **RDCG score** for each method under varying significance levels using simulated data:
```bash
python evaluation_simulated_data_rdcg.py

### Speed Test
Tests runtime performance of different search methods on simulated data:
```bash
python evaluation_simulated_data_speed.py

## Core Function

### `get_corrected_contingency_table_dict`

**Location:**  
`api.analytics.descriptive.correlation.contingency_table_correction`

**Function Signature:**

```python
get_corrected_contingency_table_dict(
    contingency_table_dict,
    target_p_value,
    delta=0.0001,
    whether_speed_up_screen=True
)


The most critical funtion to use is get_corrected_contingency_table_dict(contingency_table_dict, target_p_value, delta=0.0001, whether_speed_up_screen=True) under the folder api.analytics.descriptive.correlation.contingency_table_correction. The contingency_table_dict needs the dict format like {'n11': ##, 'n10': ##, 'n01': ##, 'n11': ##}, target_p_value is the user-specified significance level, delta specifies the accuracy in decimal place and we stop in the 4th decimal place by default, and whether_speed_up_screen control whether impliment Algorithm 4 in the paper when whether_speed_up_screen=True or impliment Algorithm 3 in the paper when whether_speed_up_screen=False.

The get_corrected_contingency_table_dict() will adjust the observed contingency table into the ECC corrected contingency table. With the ECC corrected contingency table, users can apply any existing MLE version of correlation function to find its ECC related value. For example, given the observed contingency table coded as {'n11': 100, 'n10': 100, 'n01': 200, 'n00': 600}, get_corrected_contingency_table_dict({'n11': 100, 'n10': 100, 'n01': 200, 'n00': 600}, 0.01, delta=0.0001, whether_speed_up_screen=True) will generate the ECC corrected contingency table coded as {'n11': 77.33688354492189, 'n10': 122.66311645507811, 'n01': 222.66311645507812, 'n00': 577.3368835449219} under the significance level 0.01 with the accuracy in the 4th decimal place. Take Odds Ratio = n11*n00/(n10*n01) for example, the ECC version of Odds Ratio = (77.33688354492189*577.3368835449219)/(122.66311645507811*222.66311645507812) = 1.634758834767347.



## Ongoing Development

This code is being developed on an on-going basis at the author's
[Github site](https://github.com/lian-duan-hofstra/2024.0585).

