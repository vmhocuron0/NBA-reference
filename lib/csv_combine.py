import os
import pandas as pd


class CombineCSV:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def combine_career_summary(self):
        """
        Combines all CSV files in the specified directory into one CSV file.
        """

        try:
            data_frames = []

            # Iterate over files in the directory
            for file in os.listdir(self.input_dir):
                if file.endswith(".csv"):  # Only process CSV files
                    file_path = os.path.join(self.input_dir, file)
                    print(f"Processing file: {file_path}")
                    df = pd.read_csv(file_path)

                    # Drop columns with all NA values to avoid the FutureWarning
                    df = df.dropna(axis=1, how='all')
                    data_frames.append(df)

            if data_frames:
                # Combine all DataFrames
                combined_df = pd.concat(data_frames, ignore_index=True)
                # Save the combined DataFrame to the output file
                combined_df.to_csv(self.output_dir, index=False)
                print(
                    f"All files combined successfully into: {self.output_dir}")
            else:
                print("No CSV files found in the specified directory.")
        except Exception as e:
            print(f"An error occurred: {e}")
