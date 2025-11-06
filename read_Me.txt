# Cutlery-to-Box Fitting Algorithm

Author: Attiso Bhowmick  
Date: 6 November 2025  

## Project Overview
This project presents an optimization algorithm that identifies the most suitable box for a given case of cutlery items.  
Each case contains multiple SKUs (different cutlery types). The algorithm applies geometric logic to compare item surface areas and box dimensions, ensuring efficient packing and minimal unused space.

## Problem Context
All items considered are cutlery pieces grouped into "cases," where each case can include multiple SKUs.

The algorithm follows a systematic approach:

- Identify the SKU with the largest surface area (Length × Breadth) in a case; this determines the primary box face.  
- Compare the SKU’s area against all boxes’ possible face areas (L×B, B×H, H×L).  
- Once a suitable face match is found, compute the total stacked height of all SKUs and verify whether it fits within the remaining box dimension.  
- If it fits, the corresponding box is selected; otherwise, the algorithm proceeds to the next available option.

In summary:  
The largest surface area determines the face fit, while the total height determines whether the items can stack within the box.

## Algorithm Description

### Step 1. Data Preparation
- Import and clean both CSV files (Box Data and SKU Data).  
- Split and convert dimensional data to numeric form.  
- Compute:
  - All three possible face areas for each box.  
  - Surface area (L×B) for each SKU.  

### Step 2. Case-Level Analysis
- For each case, determine the SKU with the largest surface area.  
- Calculate the total stacked height of all SKUs in that case.  

### Step 3. Box Comparison
- Compare each case against all available boxes.  
- Identify boxes whose face area can accommodate the largest SKU.  
- Record which face matched (LB, BH, or HL) and the remaining box dimension.

### Step 4. Box Selection Criteria
- Retain only boxes where the remaining dimension is greater than or equal to the total stacked height.  
- If multiple boxes qualify, choose the one with the tightest fit (smallest remaining space).  
- If none qualify, select the next-best option (largest remaining dimension that failed height).  
- If no boxes match, label the case as "No Box Found."

### Step 5. Output Generation
The final output contains the following fields:
- Case ID  
- All SKUs in the case  
- Largest SKU  
- Total stacked height  
- Selected box ID  
- Matched face type  
- Fit classification  

## Additional Notes
- Uses the copy() method during DataFrame operations to avoid pandas SettingWithCopy warnings.  
- Considers all possible box orientations (LB, BH, HL).  
- Always returns the best possible match, even when a perfect stack is not achievable.  

## Output Example

| Case ID | Largest SKU | Total Height | Chosen Box | Matched Face | Fit Type |
|----------|--------------|---------------|-------------|--------------|----------|
| C001     | SKU_12       | 45.3          | BOX_B2      | L×B          | Perfect Fit |

## Technologies Used
- Python  
- Pandas, NumPy for data handling  
- CSV-based data input  

## Future Improvements Planned:
- Add 3D visualization of fit accuracy  
- Include cost-based optimization for multi-box packing  
- Develop a web dashboard (e.g., Streamlit) for interactive analysis  
- make all possible 3D orientations of the SKUs for a more optimsed result (needs larger dataset and more time)

Developed as a practical data-driven optimization tool for packaging efficiency.

