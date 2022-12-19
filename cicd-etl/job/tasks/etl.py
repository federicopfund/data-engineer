from job.common import Task
from sklearn.datasets import fetch_california_housing
import pandas as pd


class SampleETLTask(Task):
        
        
    def main(self):
        """Main ETL script definition.

        :return: None
        """

        # log that main ETL job is starting
        log.warn('etl_job is up-and-running')

        # execute ETL pipeline
        data = extract_data(self)
        data_transformed = transform_data(data, 21)
        load_data(data_transformed)

        # log the success and terminate Spark application
        log.warn('test_etl_job is finished')
        spark.stop()
        return None


    def extract_data(self):
        """Load data from Parquet file format.

        :param self: self start session object.
        :return: Spark DataFrame.
        """
        df = (
            self
            .read
            .parquet('tests/test_data/employees'))

        return df


    def transform_data(df, steps_per_floor_):
        """Transform original dataset rename.

        :param df: Input DataFrame.
        :param steps_per_floor_: The number of steps per-floor at 43 Tanner
            Street.
        :return: Transformed DataFrame.
        """
        df_transformed = (
            df
            .select(
                col('id'),
                concat_ws(
                    ' ',
                    col('first_name'),
                    col('second_name')).alias('name'),
                (col('floor') * lit(steps_per_floor_)).alias('steps_to_desk')))

        return df_transformed


    def load_data(df):
        """Collect data locally and write to CSV.

        :param df: DataFrame to print.
        :return: None
        """
        (df
        .coalesce(1)
        .write
        .csv('loaded_data', mode='overwrite', header=True))
        return None


    def create_test_data(self, config):
        """Create un Pre-test data.

        This function creates both both pre- and post- transformation data
        saved as Parquet files in tests/test_data. This will be used for
        unit tests as well as to load as part of the example ETL job.
        :return: None
        """
        # create example data from scratch
        local_records = [
            Row(id=1, first_name='Dan', second_name='Germain', floor=1),
            Row(id=2, first_name='Dan', second_name='Sommerville', floor=1),
            Row(id=3, first_name='Alex', second_name='Ioannides', floor=2),
            Row(id=4, first_name='Ken', second_name='Lai', floor=2),
            Row(id=5, first_name='Stu', second_name='White', floor=3),
            Row(id=6, first_name='Mark', second_name='Sweeting', floor=3),
            Row(id=7, first_name='Phil', second_name='Bird', floor=4),
            Row(id=8, first_name='Kim', second_name='Suter', floor=4)
        ]

        df = self.createDataFrame(local_records)

        # write to Parquet file format
        (df
        .coalesce(1)
        .write
        .parquet('tests/test_data/employees', mode='overwrite'))

        # create transformed version of data
        df_tf = transform_data(df, config['steps_per_floor'])

        # write transformed version of data to Parquet
        (df_tf
        .coalesce(1)
        .write
        .parquet('tests/test_data/employees_report', mode='overwrite'))

        return None   
        
    
    
    def _write_data(self):
        db = self.conf["output"].get("database", "default")
        table = self.conf["output"]["table"]
        self.logger.info(f"Writing housing dataset to {db}.{table}")
        _data: pd.DataFrame = fetch_california_housing(as_frame=True).frame
        df = self.spark.createDataFrame(_data)
        df.write.format("delta").mode("overwrite").saveAsTable(f"{db}.{table}")
        self.logger.info("Dataset successfully written")

    def launch(self):
        self.logger.info("Launching sample ETL task")
        self._write_data()
        self.logger.info("Sample ETL task finished!")

# if you're using python_wheel_task, you'll need the entrypoint function to be used in setup.py
def entrypoint():  # pragma: no cover
    task = SampleETLTask()
    task.launch()
    Task.main()

# if you're using spark_python_task, you'll need the __main__ block to start the code execution
if __name__ == '__main__':
    entrypoint()
    

    