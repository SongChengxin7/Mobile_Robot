;; Auto-generated. Do not edit!


(when (boundp 'pocker_bot_vrep_description::wheel_vel)
  (if (not (find-package "POCKER_BOT_VREP_DESCRIPTION"))
    (make-package "POCKER_BOT_VREP_DESCRIPTION"))
  (shadow 'wheel_vel (find-package "POCKER_BOT_VREP_DESCRIPTION")))
(unless (find-package "POCKER_BOT_VREP_DESCRIPTION::WHEEL_VEL")
  (make-package "POCKER_BOT_VREP_DESCRIPTION::WHEEL_VEL"))

(in-package "ROS")
;;//! \htmlinclude wheel_vel.msg.html


(defclass pocker_bot_vrep_description::wheel_vel
  :super ros::object
  :slots (_left_vel _right_vel ))

(defmethod pocker_bot_vrep_description::wheel_vel
  (:init
   (&key
    ((:left_vel __left_vel) 0.0)
    ((:right_vel __right_vel) 0.0)
    )
   (send-super :init)
   (setq _left_vel (float __left_vel))
   (setq _right_vel (float __right_vel))
   self)
  (:left_vel
   (&optional __left_vel)
   (if __left_vel (setq _left_vel __left_vel)) _left_vel)
  (:right_vel
   (&optional __right_vel)
   (if __right_vel (setq _right_vel __right_vel)) _right_vel)
  (:serialization-length
   ()
   (+
    ;; float32 _left_vel
    4
    ;; float32 _right_vel
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _left_vel
       (sys::poke _left_vel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _right_vel
       (sys::poke _right_vel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _left_vel
     (setq _left_vel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _right_vel
     (setq _right_vel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get pocker_bot_vrep_description::wheel_vel :md5sum-) "74ad8f7ea4d888606e4f41069cec47ff")
(setf (get pocker_bot_vrep_description::wheel_vel :datatype-) "pocker_bot_vrep_description/wheel_vel")
(setf (get pocker_bot_vrep_description::wheel_vel :definition-)
      "float32 left_vel
float32 right_vel
")



(provide :pocker_bot_vrep_description/wheel_vel "74ad8f7ea4d888606e4f41069cec47ff")


