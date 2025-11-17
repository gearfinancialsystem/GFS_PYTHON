import os
import subprocess
import sys
from pathlib import Path


def generate_proto_code():
    """Generate gRPC Python code from .proto files"""

    # Get the project root directory
    project_root = Path(__file__).parent
    proto_dir = project_root / "protos"
    output_dir = project_root / "src" / "pygfs" / "grpc_gen"

    print(f"Project root: {project_root}")
    print(f"Proto directory: {proto_dir}")
    print(f"Output directory: {output_dir}")

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all .proto files
    proto_files = [f for f in proto_dir.iterdir() if f.suffix == '.proto']

    if not proto_files:
        print(f"No .proto files found in {proto_dir}")
        return

    for proto_file in proto_files:
        print(f"Generating code for {proto_file.name}...")

        command = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{proto_dir}",
            f"--python_out={output_dir}",
            f"--pyi_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            str(proto_file)
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error generating code for {proto_file.name}:")
            print(result.stderr)
            sys.exit(1)
        else:
            print(f"✅ Successfully generated code for {proto_file.name}")

    # Create __init__.py in grpc_gen directory
    init_file = output_dir / "__init__.py"
    init_file.write_text('''"""
Generated gRPC code from .proto files.
This module contains the auto-generated protobuf and gRPC classes.
"""

from . import helloworld_pb2
from . import helloworld_pb2_grpc

# Re-export the most commonly used classes for convenience
from .helloworld_pb2 import HelloRequest, HelloReply
from .helloworld_pb2_grpc import GreeterStub, GreeterServicer

__all__ = [
    'helloworld_pb2',
    'helloworld_pb2_grpc', 
    'HelloRequest',
    'HelloReply',
    'GreeterStub',
    'GreeterServicer',
]
''')

    # Fix import issues in generated grpc files
    fix_imports(output_dir)

    print(f"✅ Proto code generation completed! Files saved to {output_dir}")


def fix_imports(output_dir):
    """
    Fix import statements in generated gRPC files.
    """
    for file_path in output_dir.iterdir():
        if file_path.suffix == '.py':
            content = file_path.read_text()
            # Fix relative imports for helloworld
            content = content.replace(
                'import helloworld_pb2 as helloworld__pb2',
                'from . import helloworld_pb2 as helloworld__pb2'
            )
            file_path.write_text(content)


if __name__ == "__main__":
    generate_proto_code()