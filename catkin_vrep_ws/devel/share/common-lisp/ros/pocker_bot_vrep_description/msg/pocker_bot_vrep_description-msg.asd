
(cl:in-package :asdf)

(defsystem "pocker_bot_vrep_description-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "wheel_vel" :depends-on ("_package_wheel_vel"))
    (:file "_package_wheel_vel" :depends-on ("_package"))
  ))