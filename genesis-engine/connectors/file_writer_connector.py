import os

# The File Writer Connector (Secondary/Driven Adapter)

class FileWriterConnector:
    """
    Receives events containing generated code and writes them to files.
    This is a "driven" adapter because it is called by the application
    core in response to an event.
    """
    def handle(self, generated_code_events):
        """
        Handles events that contain code to be written to disk.
        """
        for event in generated_code_events:
            if event.event_type == "CodeGenerated":
                filepath = event.filepath
                content = event.content

                # Ensure the directory exists before writing the file.
                dir_name = os.path.dirname(filepath)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                    print(f"FileWriterConnector: Created directory {dir_name}")

                # Write the file.
                with open(filepath, "w") as f:
                    f.write(content)
                print(f"FileWriterConnector: Wrote file {filepath}")
