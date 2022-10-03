from ast import arg
from pickle import TRUE
from xml.dom.minidom import TypeInfo
from depthai_sdk import Previews
from depthai_sdk.managers import PipelineManager, PreviewManager
import depthai as dai
import cv2
from depthai_sdk.fps import FPSHandler


mgr = PipelineManager()
mgr.createColorCam(xout=True, fps=60, res= dai.ColorCameraProperties.SensorResolution.THE_1080_P)
mgr.createRightCam(xout=True, fps=120, res= dai.MonoCameraProperties.SensorResolution.THE_400_P)
mgr.createLeftCam(xout=True, fps=120, res= dai.MonoCameraProperties.SensorResolution.THE_400_P)
mgr.createDepth(useDisparity=True)


with dai.Device(mgr.pipeline, True) as device:
    pv = PreviewManager(display=[Previews.disparityColor.name, Previews.color.name ])
    pv.createQueues(device)
    fpsHandle = FPSHandler()
    while True:
        frame = pv.prepareFrames()
        fpsHandle.nextIter()
        fps = fpsHandle.fps()
        
        pv.showFrames(callback=print("FPS : "+ str(fps)))

        if cv2.waitKey(1) == ord('q'):
            break