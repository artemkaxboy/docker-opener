#!/usr/bin/env bats

load test_helper

setup() {
  init_debian
  stub_debian
}

teardown() {
  unstub_debian
  rm -fr "${TMP}"/*
}

@test "opener " {
  alias opener='docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener:snapshot'
  docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener:snapshot h
  assert_output --partial 'help'
}

#@test "start td-agent successfully (debian)" {
#  rm -f "${TMP}/etc/default/td-agent"
#  rm -f "${TMP}/var/run/td-agent/td-agent.pid"
#
#  stub_path /sbin/start-stop-daemon "echo; echo start-stop-daemon; for arg; do echo \"  \$arg\"; done"
#  stub log_success_msg "td-agent : true"
#
#  run_service start
#  assert_output <<EOS
#Starting td-agent:
#start-stop-daemon
#  --start
#  --quiet
#  --pidfile
#  ${TMP}/var/run/td-agent/td-agent.pid
#  --exec
#  ${TMP}/opt/td-agent/embedded/bin/ruby
#  -c
#  td-agent
#  --group
#  td-agent
#  --
#  ${TMP}/usr/sbin/td-agent
#  --log
#  ${TMP}/var/log/td-agent/td-agent.log
#  --use-v1-config
#  --daemon
#  ${TMP}/var/run/td-agent/td-agent.pid
#EOS
#  assert_success
#
#  unstub_path /sbin/start-stop-daemon
#  unstub log_success_msg
#}
