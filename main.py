"""
================================================================================
PROJECT: Cutlery-to-Box Fitting Algorithm
AUTHOR: [Attiso Bhowmick]
DATE: [6th November/ 2025]

CONTEXT:
--------
All items here are cutlery pieces packed together into "cases".
Each case can have multiple SKUs (different cutlery types).
My idea for the algorithm was simple:

> Since all are cutlery, I can find the item with the largest surface area
> (Length × Breadth) — this item primarily determines the box type.
> Then I’ll compare it against all boxes by checking their three face areas
> (Length×Breadth, Breadth×Height, Height×Length).
> Once I find a box whose face area is large enough to fit this largest SKU,
> I’ll add up the heights of all items in that case to see if they can stack
> within the box’s remaining dimension (the one not used to form the matching face).
> If they fit — great, that’s our box.
> If not, I’ll move to the next possible box match.

In short: largest area decides the face fit, total height decides whether it stacks.

ALGORITHM (Step-by-Step):

1-----Read and clean both CSV files (Box & SKU data).
    - Split and convert dimensions.
    - Compute all 3 face areas for boxes.
    - Compute surface area (L×B) for SKUs.

2-----For each case:
    - Find the SKU with the largest area.
    - Calculate total stacked height of all SKUs in that case.

3️-----Compare each case with every box:
    - Record all boxes whose face areas can fit the largest SKU.
    - Keep track of which face matched (LB/BH/HL) and the remaining box dimension.

4️------Filter matches:
    - Keep only boxes where remaining dimension ≥ total stacked height.
    - If multiple fit, choose the tightest (smallest remaining dimension).
    - If none fit, pick the next-best (largest remaining dimension that failed height).
    - If still none, mark as “No Box Found”.

5️------Output:
    - Case ID, all SKUs, largest SKU, total height, chosen box, matched face, fit type.

P.S.:
• Uses `.copy()` during DataFrame operations to avoid pandas SettingWithCopy warnings.
• Considers all possible box orientations (LB, BH, HL).
• Always returns the best possible match, even if a perfect stack isn’t possible.

================================================================================
"""


#already installed pandas in the venv
import pandas as pd

# Reading UTF formatted CSV files (since they are in the same .venv/Data folder)
box_df = pd.read_csv("Data/box dim.csv")
sku_df = pd.read_csv("Data/SKU dim.csv")
print("Box Data:\n", box_df.head(), "\n")
print("Cutlery Data:\n", sku_df.head(), "\n")
print(box_df.columns)
print(sku_df.columns)

#Data Cleaning Procedure
box_df[['LENGTH', 'BREADTH', 'HEIGHT']] = box_df['Dimensions (in inches)'].str.split('×', expand=True)
box_df[['LENGTH', 'BREADTH', 'HEIGHT']] = box_df[['LENGTH', 'BREADTH', 'HEIGHT']].astype(float)

#Calxulating all the areas now
box_df['AREA_LB'] = box_df['LENGTH'] * box_df['BREADTH']
box_df['AREA_BH'] = box_df['BREADTH'] * box_df['HEIGHT']
box_df['AREA_HL'] = box_df['HEIGHT'] * box_df['LENGTH']
sku_df['AREA'] = sku_df['LENGTH'] * sku_df['BREADTH']
print(box_df.head())
print(sku_df.head())


#Now I'll run a code to fix the highest surface area of cutlery for each case
case_groups = sku_df.groupby('CASE')
case_summary = []

for case_id, group in case_groups:
       skus = group['SKU'].tolist()
        largest_item = group.loc[group['AREA'].idxmax()]
 total_height = group['HEIGHT'].sum()

    case_summary.append({
        'CASE': case_id,
        'SKUs': ', '.join(skus),
        'Largest_SKU': largest_item['SKU'],
        'Largest_Area': largest_item['AREA'],
        'Total_Height': total_height
    })

#Summary list into a DataFrame
case_summary_df = pd.DataFrame(case_summary)

print(case_summary_df)

# Matching algorithm will now start...Get by

#Matching part 1: Box Matching Algorithm (All Possible Matches)

all_matches = []

for _, case in case_summary_df.iterrows():
    case_id = case['CASE']
    largest_area = case['Largest_Area']
    total_height = case['Total_Height']

    for _, box in box_df.iterrows():
        # Define all 3 faces and the remaining dimension (depth)
        faces = {
            'LB': {'face_area': box['AREA_LB'], 'remaining': box['HEIGHT'], 'dims': (box['LENGTH'], box['BREADTH'], box['HEIGHT'])},
            'BH': {'face_area': box['AREA_BH'], 'remaining': box['LENGTH'], 'dims': (box['BREADTH'], box['HEIGHT'], box['LENGTH'])},
            'HL': {'face_area': box['AREA_HL'], 'remaining': box['BREADTH'], 'dims': (box['HEIGHT'], box['LENGTH'], box['BREADTH'])},
        }

        for face_name, face_data in faces.items():
            # Step 1: Check if the largest cutlery area fits on the face
            if largest_area <= face_data['face_area']:
                # Step 2: Record this potential match
                all_matches.append({
                    'CASE': case_id,
                    'Box_ID': box['Box ID'],
                    'Matched_Face': face_name,
                    'Face_Area': face_data['face_area'],
                    'Remaining_Dimension': face_data['remaining'],
                    'Case_Height': total_height
                })

all_matches_df = pd.DataFrame(all_matches)

print("\nAll possible matches (before filtering by height):\n", all_matches_df)


#FInding the best fit now: Matching step 2



#Matching part 1:Select best fitting or fallback box for each case

final_box_matches = []

for case_id, group in all_matches_df.groupby('CASE'):
    total_height = group['Case_Height'].iloc[0]
        valid_height_boxes = group[group['Remaining_Dimension'] >= total_height]

    if not valid_height_boxes.empty:

        best_box = valid_height_boxes.loc[valid_height_boxes['Remaining_Dimension'].idxmin()].copy()
        best_box['Fit_Status'] = 'Perfect Fit'

    else:
        best_box = group.loc[group['Remaining_Dimension'].idxmax()].copy()
        best_box['Fit_Status'] = 'Height Exceeded (Fallback Box)'

    final_box_matches.append(best_box)


final_box_matches_df = pd.DataFrame(final_box_matches)


final_result_df = pd.merge(case_summary_df, final_box_matches_df, on='CASE', how='left')


cols_to_show = [ 'CASE', 'SKUs', 'Largest_SKU', 'Largest_Area', 'Total_Height',
    'Box_ID', 'Matched_Face', 'Face_Area', 'Remaining_Dimension', 'Fit_Status']
cols_to_show = [c for c in cols_to_show if c in final_result_df.columns]

print("\n Final Box Selections per Case (with fallback logic): (Assignment result by Attiso Bhwomick)\n")
print(final_result_df[cols_to_show].to_string(index=False))
