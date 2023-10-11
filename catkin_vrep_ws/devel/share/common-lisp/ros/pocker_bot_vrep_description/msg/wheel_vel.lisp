; Auto-generated. Do not edit!


(cl:in-package pocker_bot_vrep_description-msg)


;//! \htmlinclude wheel_vel.msg.html

(cl:defclass <wheel_vel> (roslisp-msg-protocol:ros-message)
  ((left_vel
    :reader left_vel
    :initarg :left_vel
    :type cl:float
    :initform 0.0)
   (right_vel
    :reader right_vel
    :initarg :right_vel
    :type cl:float
    :initform 0.0))
)

(cl:defclass wheel_vel (<wheel_vel>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <wheel_vel>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'wheel_vel)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pocker_bot_vrep_description-msg:<wheel_vel> is deprecated: use pocker_bot_vrep_description-msg:wheel_vel instead.")))

(cl:ensure-generic-function 'left_vel-val :lambda-list '(m))
(cl:defmethod left_vel-val ((m <wheel_vel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pocker_bot_vrep_description-msg:left_vel-val is deprecated.  Use pocker_bot_vrep_description-msg:left_vel instead.")
  (left_vel m))

(cl:ensure-generic-function 'right_vel-val :lambda-list '(m))
(cl:defmethod right_vel-val ((m <wheel_vel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pocker_bot_vrep_description-msg:right_vel-val is deprecated.  Use pocker_bot_vrep_description-msg:right_vel instead.")
  (right_vel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <wheel_vel>) ostream)
  "Serializes a message object of type '<wheel_vel>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'left_vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'right_vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <wheel_vel>) istream)
  "Deserializes a message object of type '<wheel_vel>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'left_vel) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'right_vel) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<wheel_vel>)))
  "Returns string type for a message object of type '<wheel_vel>"
  "pocker_bot_vrep_description/wheel_vel")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'wheel_vel)))
  "Returns string type for a message object of type 'wheel_vel"
  "pocker_bot_vrep_description/wheel_vel")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<wheel_vel>)))
  "Returns md5sum for a message object of type '<wheel_vel>"
  "74ad8f7ea4d888606e4f41069cec47ff")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'wheel_vel)))
  "Returns md5sum for a message object of type 'wheel_vel"
  "74ad8f7ea4d888606e4f41069cec47ff")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<wheel_vel>)))
  "Returns full string definition for message of type '<wheel_vel>"
  (cl:format cl:nil "float32 left_vel~%float32 right_vel~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'wheel_vel)))
  "Returns full string definition for message of type 'wheel_vel"
  (cl:format cl:nil "float32 left_vel~%float32 right_vel~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <wheel_vel>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <wheel_vel>))
  "Converts a ROS message object to a list"
  (cl:list 'wheel_vel
    (cl:cons ':left_vel (left_vel msg))
    (cl:cons ':right_vel (right_vel msg))
))
