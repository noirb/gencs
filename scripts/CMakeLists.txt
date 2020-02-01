install(
  FILES msg.cs.template srv.cs.template
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

catkin_install_python(
  PROGRAMS gen_cs.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
