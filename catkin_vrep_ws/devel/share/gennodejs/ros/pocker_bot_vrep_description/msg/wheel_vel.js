// Auto-generated. Do not edit!

// (in-package pocker_bot_vrep_description.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class wheel_vel {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.left_vel = null;
      this.right_vel = null;
    }
    else {
      if (initObj.hasOwnProperty('left_vel')) {
        this.left_vel = initObj.left_vel
      }
      else {
        this.left_vel = 0.0;
      }
      if (initObj.hasOwnProperty('right_vel')) {
        this.right_vel = initObj.right_vel
      }
      else {
        this.right_vel = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type wheel_vel
    // Serialize message field [left_vel]
    bufferOffset = _serializer.float32(obj.left_vel, buffer, bufferOffset);
    // Serialize message field [right_vel]
    bufferOffset = _serializer.float32(obj.right_vel, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type wheel_vel
    let len;
    let data = new wheel_vel(null);
    // Deserialize message field [left_vel]
    data.left_vel = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [right_vel]
    data.right_vel = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'pocker_bot_vrep_description/wheel_vel';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '74ad8f7ea4d888606e4f41069cec47ff';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 left_vel
    float32 right_vel
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new wheel_vel(null);
    if (msg.left_vel !== undefined) {
      resolved.left_vel = msg.left_vel;
    }
    else {
      resolved.left_vel = 0.0
    }

    if (msg.right_vel !== undefined) {
      resolved.right_vel = msg.right_vel;
    }
    else {
      resolved.right_vel = 0.0
    }

    return resolved;
    }
};

module.exports = wheel_vel;
