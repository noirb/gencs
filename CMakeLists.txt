cmake_minimum_required(VERSION 2.8.3)
project(gencs)
find_package(catkin REQUIRED COMPONENTS genmsg)

catkin_package(
  CATKIN_DEPENDS genmsg
  CFG_EXTRAS gencs-extras.cmake
)

add_subdirectory(scripts)

file(WRITE ${CATKIN_DEVEL_PREFIX}/${GENMSG_LANGS_DESTINATION}/gencs "C#")
install(
  FILES ${CATKIN_DEVEL_PREFIX}/${GENMSG_LANGS_DESTINATION}/gencs
  DESTINATION ${GENMSG_LANGS_DESTINATION}
)

catkin_python_setup()
