#!/usr/bin/env python3
"""
Simple test for antsApplyTransforms with .nii files
Demonstrates current apply_transforms.py working with pydra
"""

import os
import sys
from pathlib import Path

# Use the working version
sys.path.insert(0, '/home/uqahonne/git_arush/pydra-tasks-ants')
from fileformats.medimage import Nifti1
from pydra.tasks.ants.v2.resampling.apply_transforms import ApplyTransforms

def setup_ants():
    """Setup ANTs environment"""
    os.environ['PATH'] = "/home/uqahonne/uq/ants-2.6.2-ubuntu-22.04-X64-gcc/ants-2.6.2/bin:" + os.environ.get('PATH', '')

def clear_cache():
    """Clear pydra cache"""
    import shutil
    cache_dir = Path.home() / ".cache" / "pydra"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        print(f"🧹 Cleared cache: {cache_dir}")

def test_apply_transforms():
    """Test antsApplyTransforms with real data"""

    # Setup
    setup_ants()
    clear_cache()
    os.chdir('/home/uqahonne/uq/nif/AIS/pydra-tasks-ants')

    # Input files (real medical imaging data)
    moving_path = "test_output/nii_files/moving.nii"
    reference_path = "test_output/nii_files/fixed.nii"

    # Check files exist
    if not Path(moving_path).exists():
        print(f" Missing: {moving_path}")
        return False
    if not Path(reference_path).exists():
        print(f" Missing: {reference_path}")
        return False

    # File info
    moving_size = Path(moving_path).stat().st_size / (1024*1024)
    reference_size = Path(reference_path).stat().st_size / (1024*1024)

    print(f"📊 Real Data:")
    print(f"   Moving: {moving_path} ({moving_size:.1f} MB)")
    print(f"   Reference: {reference_path} ({reference_size:.1f} MB)")

    try:
        # Create pydra task
        task = ApplyTransforms()

        # Set inputs
        task.input_image = Nifti1(moving_path)
        task.reference_image = Nifti1(reference_path)
        task.transforms = "identity"
        task.interpolation = "Linear"
        task.dimension = 3

        # Set output
        output_path = os.path.abspath("antsApplyTransforms_result.nii")
        task.output_image = output_path

        print(f"   Transform: {task.transforms}")
        print(f"   Interpolation: {task.interpolation}")
        print(f"   Dimension: {task.dimension}")
        print(f"   Output: {Path(output_path).name}")

        print(f"\n Generated ANTs Command:")
        print(f"   {task.cmdline}")

        # Execute
        print(f"\n⚡ Executing antsApplyTransforms...")
        result = task()

        # Check result
        print(f"   Return code: {result.return_code}")

        if result.stderr:
            print(f"   stderr: {result.stderr}")
        if result.stdout:
            print(f"   stdout: {result.stdout}")

        # Check output using correct pydra result access
        pydra_output = result.output_image  # Direct attribute access
        print(f"   Pydra output path: {pydra_output}")

        if Path(pydra_output).exists():
            output_size = Path(pydra_output).stat().st_size / (1024*1024)
            print(f"\n SUCCESS!")
            print(f"   Output file: {Path(pydra_output).name}")
            print(f"   Output size: {output_size:.1f} MB")
            return True
        else:
            print(f"\nOutput file not created")
            return False

    except Exception as e:
        print(f"\n Error: {e}")
        return False

if __name__ == "__main__":
    print("antsApplyTransforms Pydra testing.. ")
    print("=" * 50)

    success = test_apply_transforms()

    if success:
        print(f"..antsApplyTransforms working..")
    else:
        print(f"\nTest failed")

    sys.exit(0 if success else 1)