from flask_restful import Resource
from flask import jsonify, request

from glob import glob
import shutil
import torch
from time import strftime
import os, sys, time
from argparse import ArgumentParser

from app.sadtalker.utils.preprocess import CropAndExtract
from app.sadtalker.test_audio2coeff import Audio2Coeff
from app.sadtalker.facerender.animate import AnimateFromCoeff
from app.sadtalker.generate_batch import get_data
from app.sadtalker.generate_facerender_batch import get_facerender_data
from app.sadtalker.utils.init_path import init_path


class GenerateVideo(Resource):
    def post(self):
        print('---')
        # req = request.get_json()
        args = {
            "driven_audio": './app/sadtalker/examples/driven_audio/bus_chinese.wav',  # path to driven audio
            "source_image": './app/sadtalker/examples/source_image/full_body_1.png',  # path to source image
            "ref_eyeblink": None,  # path to reference video providing eye blinking
            "ref_pose": None,  # path to reference video providing pose
            "checkpoint_dir": './app/sadtalker/checkpoints',  # path to output
            "result_dir": './app/sadtalker/results',  # path to output
            "pose_style": 0,  # type=int, input pose style from [0, 46]
            "batch_size": 2,  # type=int, the batch size of facerender
            "size": 256,  # type=int, the image size of the facerender
            "expression_scale": 1.,  # type=float, the batch size of facerender
            "input_yaw": None,  # type=int, the input yaw degree of the user
            "input_pitch": None,  # type=int, the input pitch degree of the user
            "input_roll": None,  # type=int, the input roll degree of the user
            "enhancer": None,  # type=str, Face enhancer, [gfpgan, RestoreFormer]
            "background_enhancer": None,  # type=str, background enhancer, [realesrgan]
            "cpu": None,
            "face3dvis": None,  # generate 3d face and 3d landmarks
            "still": None,  # caniginal videos for the full body aniamtion
            "preprocess": 'crop',
            # choices=['crop', 'extcrop', 'resize', 'full', 'extfull'], how to preprocess the images
            "verbose": None,  # not
            "old_version": None,  # use the pth other than safetensor version

            # net structure and parameters
            "net_recon": 'resnet50',
            # type=str, choices=['resnet18', 'resnet34', 'resnet50'], help='useless'
            "init_path": None,  # type=str, help='Useless'
            "use_last_fc": False,  # zero initialize the last fc
            "bfm_folder": './app/sadtalker/checkpoints/BFM_Fitting/',
            "bfm_model": 'BFM_model_front.mat',  # help='bfm model'

            # default renderer parameters
            "focal": 1015.,  # type=float, default=1015.
            "center": 112.,  # type=float, default=112.
            "camera_d": 10.,  # type=float, default=10.
            "z_near": 5.,  # type=float, default=5.
            "z_far": 15.,  # type=float, default=15.
        }
        print('=== ', args)

        if torch.cuda.is_available() and not args["cpu"]:
            args["device"] = "cuda"
        else:
            args["device"] = "cpu"

        # torch.backends.cudnn.enabled = False

        pic_path = args["source_image"]
        audio_path = args["driven_audio"]
        save_dir = os.path.join(args["result_dir"], strftime("%Y_%m_%d_%H.%M.%S"))
        os.makedirs(save_dir, exist_ok=True)
        pose_style = args["pose_style"]
        device = args["device"]
        batch_size = args["batch_size"]
        input_yaw_list = args["input_yaw"]
        input_pitch_list = args["input_pitch"]
        input_roll_list = args["input_roll"]
        ref_eyeblink = args["ref_eyeblink"]
        ref_pose = args["ref_pose"]

        # current_root_path = os.path.split(sys.argv[0])[0]
        current_root_path = './app'

        sadtalker_paths = init_path(args["checkpoint_dir"], os.path.join(current_root_path, 'sadtalker/config'), args["size"],
                                    args["old_version"], args["preprocess"])

        # init model
        preprocess_model = CropAndExtract(sadtalker_paths, device)

        audio_to_coeff = Audio2Coeff(sadtalker_paths, device)

        animate_from_coeff = AnimateFromCoeff(sadtalker_paths, device)

        # crop image and extract 3dmm from image
        first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
        os.makedirs(first_frame_dir, exist_ok=True)
        print('3DMM Extraction for source image')
        first_coeff_path, crop_pic_path, crop_info = preprocess_model.generate(pic_path, first_frame_dir,
                                                                               args["preprocess"],
                                                                               source_image_flag=True,
                                                                               pic_size=args["size"])
        if first_coeff_path is None:
            print("Can't get the coeffs of the input")
            return

        if ref_eyeblink is not None:
            ref_eyeblink_videoname = os.path.splitext(os.path.split(ref_eyeblink)[-1])[0]
            ref_eyeblink_frame_dir = os.path.join(save_dir, ref_eyeblink_videoname)
            os.makedirs(ref_eyeblink_frame_dir, exist_ok=True)
            print('3DMM Extraction for the reference video providing eye blinking')
            ref_eyeblink_coeff_path, _, _ = preprocess_model.generate(ref_eyeblink, ref_eyeblink_frame_dir,
                                                                      args["preprocess"], source_image_flag=False)
        else:
            ref_eyeblink_coeff_path = None

        if ref_pose is not None:
            if ref_pose == ref_eyeblink:
                ref_pose_coeff_path = ref_eyeblink_coeff_path
            else:
                ref_pose_videoname = os.path.splitext(os.path.split(ref_pose)[-1])[0]
                ref_pose_frame_dir = os.path.join(save_dir, ref_pose_videoname)
                os.makedirs(ref_pose_frame_dir, exist_ok=True)
                print('3DMM Extraction for the reference video providing pose')
                ref_pose_coeff_path, _, _ = preprocess_model.generate(ref_pose, ref_pose_frame_dir, args["preprocess"],
                                                                      source_image_flag=False)
        else:
            ref_pose_coeff_path = None

        # audio2ceoff
        batch = get_data(first_coeff_path, audio_path, device, ref_eyeblink_coeff_path, still=args["still"])
        coeff_path = audio_to_coeff.generate(batch, save_dir, pose_style, ref_pose_coeff_path)

        # 3dface render
        if args["face3dvis"]:
            from app.sadtalker.face3d.visualize import gen_composed_video
            gen_composed_video(args, device, first_coeff_path, coeff_path, audio_path,
                               os.path.join(save_dir, '3dface.mp4'))

        # coeff2video
        data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path,
                                   batch_size, input_yaw_list, input_pitch_list, input_roll_list,
                                   expression_scale=args["expression_scale"], still_mode=args["still"],
                                   preprocess=args["preprocess"], size=args["size"])

        result = animate_from_coeff.generate(data, save_dir, pic_path, crop_info,
                                             enhancer=args["enhancer"], background_enhancer=args["background_enhancer"],
                                             preprocess=args["preprocess"], img_size=args["size"])

        shutil.move(result, save_dir + '.mp4')
        print('The generated video is named:', save_dir + '.mp4')

        if not args["verbose"]:
            shutil.rmtree(save_dir)
        pass
