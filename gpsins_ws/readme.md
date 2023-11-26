ekf_localization_node.cpp merely runs the runs the ekf_navigation_node.
# dependencies
git clone -b kinetic-devel https://github.com/cra-ros-pkg/robot_localization.git
Publishers/Subscribers:

  Subscribers:
     2. odomTopic: subscriber to odometry data
     3. twistTopic: subscriber to twist data
     4. imuTopic: subscriber to imu data

  Publishers:
     1."odometry/filtered": publishes the filtered odometry data


---
https://docs.ros.org/en/melodic/api/robot_localization/html/index.html

## sensor_msgs/Imu Message
``` yaml
Header header

geometry_msgs/Quaternion orientation
float64[9] orientation_covariance # Row major about x, y, z axes

geometry_msgs/Vector3 angular_velocity
float64[9] angular_velocity_covariance # Row major about x, y, z axes

geometry_msgs/Vector3 linear_acceleration
float64[9] linear_acceleration_covariance # Row major x, y z 
```

----
https://docs.ros.org/en/kinetic/api/robot_localization/html/navsat_transform_node.html

## sensor_msgs/NavSatFix.msg
```yaml
# Navigation Satellite fix for any Global Navigation Satellite System
#
# Specified using the WGS 84 reference ellipsoid

# header.stamp specifies the ROS time for this measurement (the corresponding satellite time may be reported using the
#        sensor_msgs/TimeReference message).
#
# header.frame_id is the frame of reference reported by the satellite receiver, usually the location of the antenna.  This is a
#        Euclidean frame relative to the vehicle, not a reference ellipsoid.
Header header

# satellite fix status information
NavSatStatus status

# Latitude [degrees]. Positive is north of equator; negative is south.
float64 latitude

# Longitude [degrees]. Positive is east of prime meridian; negative is west.
float64 longitude

# Altitude [m]. Positive is above the WGS 84 ellipsoid (quiet NaN if no altitude is available).
float64 altitude

# Position covariance [m^2] defined relative to a tangential plane through the reported position. The components are East, North, and
# Up (ENU), in row-major order.

float64[9] position_covariance

# If the covariance of the fix is known, fill it in completely. If the GPS receiver provides the variance of each measurement, put them along the diagonal. If only Dilution of Precision is available, estimate an approximate covariance from that.

uint8 COVARIANCE_TYPE_UNKNOWN = 0
uint8 COVARIANCE_TYPE_APPROXIMATED = 1
uint8 COVARIANCE_TYPE_DIAGONAL_KNOWN = 2
uint8 COVARIANCE_TYPE_KNOWN = 3

uint8 position_covariance_type
```