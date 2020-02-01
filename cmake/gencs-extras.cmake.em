@[if DEVELSPACE]@
# bin and template dir variables in develspace
set(GENCS_BIN "@(CMAKE_CURRENT_SOURCE_DIR)/scripts/gen_cs.py")
set(GENCS_TEMPLATE_DIR "@(CMAKE_CURRENT_SOURCE_DIR)/scripts")
@[else]@
# bin and template dirs in installspace
set(GENCS_BIN "${gencs_DIR}/../../../@(CATKIN_PACKAGE_BIN_DESTINATION)/gen_cs.py")
set(GENCS_TEMPLATE_DIR "${gencs_DIR}/..")
@[end if]@

# Generate .msg->.cs for C#
# The generated .cs files should be added to ALL_GEN_OUTPUT_FILES_cs
macro(_generate_msg_cs ARG_PKG ARG_MSG ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  file(MAKE_DIRECTORY ${ARG_GEN_OUTPUT_DIR})

  # Create input & output filenames
  get_filename_component(MSG_NAME ${ARG_MSG} NAME)
  get_filename_component(MSG_SHORT_NAME ${ARG_MSG} NAME_WE)

  set(MSG_GENERATED_NAME ${MSG_SHORT_NAME}.cs)
  set(GEN_OUTPUT_FILE ${ARG_GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})

  assert(CATKIN_ENV)
  add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
    DEPENDS ${GENCS_BIN} ${ARG_MSG} ${ARG_MSG_DEPS} "${GENCS_TEMPLATE_DIR}/msg.cs.template" ${ARGN}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENCS_BIN} ${ARG_MSG}
    ${ARG_IFLAGS}
    -p ${ARG_PKG}
    -o ${ARG_GEN_OUTPUT_DIR}
    -e ${GENCS_TEMPLATE_DIR}
    COMMENT "Generating C# code from ${ARG_PKG}/${MSG_NAME}"
    )
  list(APPEND ALL_GEN_OUTPUT_FILES_cs ${GEN_OUTPUT_FILE})

  gencs_append_include_dirs()
endmacro()

#gencs uses the same program to generate srv and msg files, so call the same macro
macro(_generate_srv_cs ARG_PKG ARG_SRV ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  _generate_msg_cs(${ARG_PKG} ${ARG_SRV} "${ARG_IFLAGS}" "${ARG_MSG_DEPS}" ${ARG_GEN_OUTPUT_DIR} "${GENCS_TEMPLATE_DIR}/srv.cs.template")
endmacro()

macro(_generate_module_cs)
  # do nothing
endmacro()

set(gencs_INSTALL_DIR include/csharp)

macro(gencs_append_include_dirs)
  if(NOT gencs_APPENDED_INCLUDE_DIRS)
    include_directories(BEFORE ${CATKIN_DEVEL_PREFIX}/${gencs_INSTALL_DIR})
    list(APPEND ${PROJECT_NAME}_INCLUDE_DIRS ${CATKIN_DEVEL_PREFIX}/${gencs_INSTALL_DIR})
    set(gencs_APPENDED_INCLUDE_DIRS TRUE)
  endif()
endmacro()

