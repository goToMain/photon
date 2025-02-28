#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=x86_64

source common.sh

# Docker images for calico-node, calico-cni
fn="${SPEC_DIR}/calico/calico.spec"
CALICO_VER=$(get_spec_ver "${fn}")
CALICO_VER_REL=${CALICO_VER}-$(get_spec_rel "${fn}")
CALICO_RPM=calico-${CALICO_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_RPM}

fn="${SPEC_DIR}/calico-bgp-daemon/calico-bgp-daemon.spec"
CALICO_BGP_VER=$(get_spec_ver "${fn}")
CALICO_BGP_VER_REL=${CALICO_BGP_VER}-$(get_spec_rel "${fn}")
CALICO_BGP_RPM=calico-bgp-daemon-${CALICO_BGP_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_BGP_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_BGP_RPM}

fn="${SPEC_DIR}/gobgp/gobgp.spec"
GO_BGP_VER=$(get_spec_ver "${fn}")
GO_BGP_VER_REL=${GO_BGP_VER}-$(get_spec_rel "${fn}")
GO_BGP_RPM=gobgp-${GO_BGP_VER_REL}${DIST_TAG}.${ARCH}.rpm
GO_BGP_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${GO_BGP_RPM}

fn="${SPEC_DIR}/calico-bird/calico-bird.spec"
CALICO_BIRD_VER=$(get_spec_ver "${fn}")
CALICO_BIRD_VER_REL=${CALICO_BIRD_VER}-$(get_spec_rel "${fn}")
CALICO_BIRD_RPM=calico-bird-${CALICO_BIRD_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_BIRD_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_BIRD_RPM}

fn="${SPEC_DIR}/confd/confd.spec"
CONFD_VER=$(get_spec_ver "${fn}")
CONFD_VER_REL=${CONFD_VER}-$(get_spec_rel "${fn}")
CONFD_RPM=confd-${CONFD_VER_REL}${DIST_TAG}.${ARCH}.rpm
CONFD_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CONFD_RPM}

fn="${SPEC_DIR}/calico-felix/calico-felix.spec"
CALICO_FELIX_VER=$(get_spec_ver "${fn}")
CALICO_FELIX_VER_REL=${CALICO_FELIX_VER}-$(get_spec_rel "${fn}")
CALICO_FELIX_RPM=calico-felix-${CALICO_FELIX_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_FELIX_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_FELIX_RPM}

fn="${SPEC_DIR}/calico-libnetwork/calico-libnetwork.spec"
CALICO_LIBNET_VER=$(get_spec_ver "${fn}")
CALICO_LIBNET_VER_REL=${CALICO_LIBNET_VER}-$(get_spec_rel "${fn}")
CALICO_LIBNET_RPM=calico-libnetwork-${CALICO_LIBNET_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_LIBNET_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_LIBNET_RPM}

fn="${SPEC_DIR}/calico-cni/calico-cni.spec"
CALICO_CNI_VER=$(get_spec_ver "${fn}")
CALICO_CNI_VER_REL=${CALICO_CNI_VER}-$(get_spec_rel "${fn}")
CALICO_CNI_RPM=calico-cni-${CALICO_CNI_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_CNI_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_CNI_RPM}

fn="${SPEC_DIR}/cni/cni.spec"
K8S_CNI_VER=$(get_spec_ver "${fn}")
K8S_CNI_VER_REL=${K8S_CNI_VER}-$(get_spec_rel "${fn}")
K8S_CNI_RPM=cni-${K8S_CNI_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_CNI_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${K8S_CNI_RPM}

fn="${SPEC_DIR}/calico-k8s-policy/calico-k8s-policy.spec"
CALICO_K8S_POLICY_VER=$(get_spec_ver "${fn}")
CALICO_K8S_POLICY_VER_REL=${CALICO_K8S_POLICY_VER}-$(get_spec_rel "${fn}")
CALICO_K8S_POLICY_RPM=calico-k8s-policy-${CALICO_K8S_POLICY_VER_REL}${DIST_TAG}.${ARCH}.rpm
CALICO_K8S_POLICY_RPM_FILE=${STAGE_DIR}/RPMS/$ARCH/${CALICO_K8S_POLICY_RPM}

if [ ! -f ${CALICO_RPM_FILE} ]; then
  echo "Calico RPM ${CALICO_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CALICO_BGP_RPM_FILE} ]; then
  echo "Calico BGP RPM ${CALICO_BGP_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${GO_BGP_RPM_FILE} ]; then
  echo "GoBGP RPM ${GO_BGP_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CALICO_BIRD_RPM_FILE} ]; then
  echo "Calico BIRD RPM ${CALICO_BIRD_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CONFD_RPM_FILE} ]; then
  echo "confd RPM ${CONFD_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CALICO_FELIX_RPM_FILE} ]; then
  echo "Calico felix RPM ${CALICO_FELIX_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CALICO_LIBNET_RPM_FILE} ]; then
  echo "Calico libnetwork RPM ${CALICO_LIBNET_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CALICO_CNI_RPM_FILE} ]; then
  echo "Calico CNI RPM ${CALICO_CNI_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${K8S_CNI_RPM_FILE} ]; then
  echo "K8S CNI RPM ${K8S_CNI_RPM_FILE} not found. Exiting.."
  exit 1
fi

if [ ! -f ${CALICO_K8S_POLICY_RPM_FILE} ]; then
  echo "Calico k8s policy RPM ${CALICO_K8S_POLICY_RPM_FILE} not found. Exiting.."
  exit 1
fi

CALICO_NODE_IMG_NAME=vmware/photon-${DIST_VER}-calico-node:v${CALICO_VER}
CALICO_CNI_IMG_NAME=vmware/photon-${DIST_VER}-calico-cni:v${CALICO_CNI_VER}
CALICO_K8S_POLICY_IMG_NAME=vmware/photon-${DIST_VER}-calico-kube-policy-controller:v${CALICO_K8S_POLICY_VER}
CALICO_NODE_TAR=calico-node-v${CALICO_VER_REL}.tar
CALICO_CNI_TAR=calico-cni-v${CALICO_CNI_VER_REL}.tar
CALICO_K8S_POLICY_TAR=calico-k8s-policy-v${CALICO_K8S_POLICY_VER_REL}.tar

NODE_IMG_ID=$(docker images -q ${CALICO_NODE_IMG_NAME} 2> /dev/null)
if [[ ! -z "${NODE_IMG_ID}" ]]; then
  echo "Removing image ${CALICO_NODE_IMG_NAME}"
  docker rmi -f ${CALICO_NODE_IMG_NAME}
fi

CNI_IMG_ID=$(docker images -q ${CALICO_CNI_IMG_NAME} 2> /dev/null)
if [[ ! -z "${CNI_IMG_ID}" ]]; then
  echo "Removing image ${CALICO_CNI_IMG_NAME}"
  docker rmi -f ${CALICO_CNI_IMG_NAME}
fi

mkdir -p tmp/calico

cp ${CALICO_RPM_FILE} \
   ${CALICO_BGP_RPM_FILE} \
   ${GO_BGP_RPM_FILE} \
   ${CALICO_BIRD_RPM_FILE} \
   ${CONFD_RPM_FILE} \
   ${CALICO_FELIX_RPM_FILE} \
   ${CALICO_LIBNET_RPM_FILE} \
   ${CALICO_CNI_RPM_FILE} \
   ${K8S_CNI_RPM_FILE} \
   ${CALICO_K8S_POLICY_RPM_FILE} \
   tmp/calico/

pushd ./tmp/calico
cmd="cd '${PWD}' && \
rpm2cpio '${CALICO_RPM}' | cpio -vid && \
rpm2cpio '${CALICO_BGP_RPM}' | cpio -vid && \
rpm2cpio '${GO_BGP_RPM}' | cpio -vid && \
rpm2cpio '${CALICO_BIRD_RPM}' | cpio -vid && \
rpm2cpio '${CONFD_RPM}' | cpio -vid && \
rpm2cpio '${CALICO_FELIX_RPM}' | cpio -vid && \
rpm2cpio '${CALICO_LIBNET_RPM}' | cpio -vid && \
rpm2cpio '${CALICO_CNI_RPM}' | cpio -vid && \
rpm2cpio '${K8S_CNI_RPM}' | cpio -vid && \
rpm2cpio '${CALICO_K8S_POLICY_RPM}' | cpio -vid"

if ! rpmSupportsZstd; then
  docker run --rm --privileged -v ${PWD}:${PWD} $PH_BUILDER_TAG bash -c "${cmd}"
else
  eval "${cmd}"
fi
popd

start_repo_server

docker build --rm -t ${CALICO_NODE_IMG_NAME} -f Dockerfile.calico-node .
docker save -o ${CALICO_NODE_TAR} ${CALICO_NODE_IMG_NAME}
gzip ${CALICO_NODE_TAR}
mv -f ${CALICO_NODE_TAR}.gz ${STAGE_DIR}/docker_images/

docker build --rm -t ${CALICO_CNI_IMG_NAME} -f Dockerfile.calico-cni .
docker save -o ${CALICO_CNI_TAR} ${CALICO_CNI_IMG_NAME}
gzip ${CALICO_CNI_TAR}
mv -f ${CALICO_CNI_TAR}.gz ${STAGE_DIR}/docker_images/

docker build --rm -t ${CALICO_K8S_POLICY_IMG_NAME} -f Dockerfile.calico-k8s-policy .
docker save -o ${CALICO_K8S_POLICY_TAR} ${CALICO_K8S_POLICY_IMG_NAME}
gzip ${CALICO_K8S_POLICY_TAR}
mv -f ${CALICO_K8S_POLICY_TAR}.gz ${STAGE_DIR}/docker_images/

rm -rf ./tmp
