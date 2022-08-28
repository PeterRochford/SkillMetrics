from PIL import Image
import numpy as np
import subprocess
import argparse
import glob
import os

import pandas  # this script does not use pandas, but import it to ensure the
               #    functionality of the others


# ## CONSTANTS ################################################################## #

IMAGES_FORMAT = ".png"
EXAMPLES_FOLDER_NAME = 'Examples'
SCRIPTS_TESTED = ("taylor*[0-9].py", )  # ("target*.py", "taylor*.py")
PYTHON_COMMAND = "python <SCRIPT> -noshow"
DEBUG_FILE_NAME = "<BASE>%s" % IMAGES_FORMAT
EXAMP_FILE_NAME = "<BASE>_example%s" % IMAGES_FORMAT


# ## DEFS ####################################################################### #

def change_cwd() -> None:
    """
    Move the current working directory (cwd) to the Examples folder
    """

    test_folder_path = os.path.dirname(os.path.realpath(__file__))
    base_folder_path = os.path.split(test_folder_path)[0]
    examples_folder_path = os.path.join(base_folder_path, EXAMPLES_FOLDER_NAME)
    os.chdir(examples_folder_path)

    return None


def get_scripts_to_run() -> tuple:
    """
    List scripts files that produce plots
    """

    ret_list = []
    for tested_glob in SCRIPTS_TESTED:
        ret_list += glob.glob(tested_glob)
        del tested_glob
    return tuple(ret_list)


def get_comparable_pixels_rgba(file_path_1: str, file_path_2: str) -> tuple:
    """
    Read image files and get them in the same shape
    :return: (nd array with RGBA of arg 1, nd array with RGBA of arg2, bool if
                images were resized)
    """

    # open image files and get 2D dimensions
    img_prev, img_curr = Image.open(file_path_1), Image.open(file_path_2)
    pixels_prev, pixels_curr = img_prev.__array__(), img_curr.__array__()
    shape_prev, shape_curr = pixels_prev.shape, pixels_curr.shape

    # files have equal size then nothing needs to be done
    if sum([1 if p != c else 0 for p, c in zip(shape_prev, shape_curr)]) == 0:
        img_prev.close(), img_curr.close()
        return pixels_prev, pixels_curr, False

    # get the sizes of the smallest
    min_x = min(shape_prev[0], shape_curr[0])
    min_y = min(shape_prev[1], shape_curr[1])
    
    # reshape both images
    min_xy = (min_y, min_x)
    img_prev, img_curr = img_prev.resize(min_xy), img_curr.resize(min_xy)

    # crop both images
    # box_xy = (0, 0, min_y, min_x)
    # img_prev, img_curr = img_prev.crop(box_xy), img_curr.crop(box_xy)

    # get and close
    pixels_prev, pixels_curr = img_prev.__array__(), img_curr.__array__()
    img_prev.close(), img_curr.close()

    return pixels_prev, pixels_curr, True


def compare_rasters_pixelwise(prev: str, curr: str) -> tuple:
    """
    
    :param prev:
    :param curr:
    :return: Percentual color distance between images, boolean flag if images were
                resized if comparison was possible, raise errors otherwise
    """

    try:
        pixels_prev, pixels_curr, resized = get_comparable_pixels_rgba(prev, curr)

        # get images 'intensities' (color magnitude)
        pixels_maginitude_1, pixels_maginitude_2 = np.sum(pixels_prev), np.sum(pixels_curr)
        pixels_maginitude_mean = np.mean([pixels_maginitude_1, pixels_maginitude_2])
        del pixels_maginitude_1, pixels_maginitude_2

        # get pixels percentual distance
        pixels_dist = np.sum(pixels_prev - pixels_curr)
        pixels_dist_pct = 100 * pixels_dist / pixels_maginitude_mean
        del pixels_dist, pixels_maginitude_mean
        
        return pixels_dist_pct, resized
        
    except FileNotFoundError as e:
        print("  ", e)
        raise e


def evaluate_output(all_script_file_names: tuple, clean_files: bool) -> None:
    """
    
    :param all_script_file_names:
    :param clean_files:
    :return: None
    """

    print("Executing %d scripts in sequence:" % len(all_script_file_names))

    for script_count, script_file_name in enumerate(all_script_file_names):

        # get new and old filenames
        output_file_name = script_file_name[0:-3]
        output_file_name_new = DEBUG_FILE_NAME.replace("<BASE>", output_file_name)
        output_file_name_old = EXAMP_FILE_NAME.replace("<BASE>", output_file_name)
        del output_file_name    

        # define command to execute
        py_command = PYTHON_COMMAND.replace("<SCRIPT>", script_file_name)

        if os.path.exists(output_file_name_old):
            
            # run the command and calculate files distance
            subprocess.run(py_command, shell=True, stdout=subprocess.DEVNULL)
            rasters_distance_pct, resized = compare_rasters_pixelwise(
                output_file_name_old, output_file_name_new)

            # communicate result
            print(" %02d: %6.02f%% distance between '%s' and '%s'%s." % 
                (script_count+1, rasters_distance_pct, output_file_name_old,
                 output_file_name_new, " (size adjusted)" if resized else ""))

            del rasters_distance_pct, resized

        else:
            # if old image file does not exist, skip
            print(" %02d. Skipping '%s': base figure not found." % 
                (script_count+1, script_file_name))
        
        # delete new file if needed
        if clean_files and os.path.exists(output_file_name_new):
            os.remove(output_file_name_new)

        del output_file_name_new, output_file_name_old
        del script_count, script_file_name

    return None


# ## MAIN ####################################################################### #

if __name__ == '__main__':

    # Defines the output file name or path 
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-clean_files', dest='clean_files', action='store_true',
                            help="Delete new files if this flag is present.")
    args = arg_parser.parse_args()
    del arg_parser

    # Move to the Examples folder
    change_cwd()

    # list scripts to execute
    test_script_file_names = get_scripts_to_run()

    # execute each one
    evaluate_output(test_script_file_names, args.clean_files)

    # wrapping up message
    new_files_were = "deleted" if args.clean_files else "kept"
    print("New files were %s after comparison." % new_files_were)
