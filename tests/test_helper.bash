export TMP="${BATS_TEST_DIRNAME}/tmp"

ORIG_PATH="${PATH}"
PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"
PATH="${TMP}/bin:${PATH}"
export PATH

# unset td-agent configuration variables
unset DAEMON_ARGS
unset NAME
unset PIDFILE
unset STOPTIMEOUT
unset TD_AGENT_ARGS
unset TD_AGENT_BIN_FILE
unset TD_AGENT_DEFAULT
unset TD_AGENT_GROUP
unset TD_AGENT_HOME
unset TD_AGENT_LOCK_FILE
unset TD_AGENT_LOG_FILE
unset TD_AGENT_NAME
unset TD_AGENT_PID_FILE
unset TD_AGENT_RUBY
unset TD_AGENT_USER
unset name
unset process_bin
unset prog

init_debian() {
  mkdir -p "${TMP}/var/run/td-agent"
}

stub_debian() {
  stub getent "passwd : echo td-agent:x:500:500:,,,:/var/lib/td-agent:/sbin/nologin"
  stub chown "true" \
             "true"
  stub getent "group : echo td-agent:x:500:"
}

unstub_debian() {
  unstub getent
  unstub chown
}

teardown() {
  rm -fr "${TMP}"/*
}

stub() {
  local program="$1"
  local prefix="$(echo "$program" | tr a-z- A-Z_)"
  shift

  export "${prefix}_STUB_PLAN"="${TMP}/${program}-stub-plan"
  export "${prefix}_STUB_RUN"="${TMP}/${program}-stub-run"
  export "${prefix}_STUB_END"=

  mkdir -p "${TMP}/bin"
  ln -sf "${BATS_TEST_DIRNAME}/stubs/stub" "${TMP}/bin/${program}"

  touch "${TMP}/${program}-stub-plan"
  for arg in "$@"; do printf "%s\n" "$arg" >> "${TMP}/${program}-stub-plan"; done
}

unstub() {
  local program="$1"
  local prefix="$(echo "$program" | tr a-z- A-Z_)"
}

stub_path() {
  local path="$1"
  local name="${path##*/}"
  shift 1
  stub "${name}" "$@"
  mv -f "${TMP}/bin/${name}" "${TMP}/${path#/}"
}

unstub_path() {
  local path="$1"
  local name="${path##*/}"
  shift 1
  mv -f "${TMP}/${path#/}" "${TMP}/bin/${name}"
  unstub "${name}"
}

assert() {
  if ! "$@"; then
    flunk "failed: $@"
  fi
}

flunk() {
  { if [ "$#" -eq 0 ]; then cat -
    else echo "$@"
    fi
  } | sed "s:${TMP}:\${TMP}:g" >&2
  return 1
}

assert_success() {
  if [ "$status" -ne 0 ]; then
    { echo "command failed with exit status $status"
      echo "output: $output"
    } | flunk
  elif [ "$#" -gt 0 ]; then
    assert_output "$1"
  fi
}

assert_failure() {
  if [ "$status" -eq 0 ]; then
    flunk "expected failed exit status"
  elif [ "$#" -gt 0 ]; then
    assert_output "$1"
  fi
}

assert_equal() {
  if [ "$1" != "$2" ]; then
    { echo "expected: $1"
      echo "actual:   $2"
      echo "diff:"
      diff -u <(echo "$1") <(echo "$2")
    } | flunk
  fi
}

assert_output() {
  local expected
  if [ $# -eq 0 ]; then expected="$(cat -)"
  else expected="$1"
  fi
  assert_equal "$expected" "$output"
}

run_service() {
  run "${TMP}/etc/init.d/td-agent" "$@"
}
