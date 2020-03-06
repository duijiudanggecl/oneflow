#include "oneflow/core/vm/vm_stream.msg.h"
#include "oneflow/core/common/util.h"

namespace oneflow {

ObjectMsgPtr<VmInstrChain> VmStream::NewVmInstrChain(VmInstructionMsg* vm_instr_msg) {
  if (free_chain_list().empty()) {
    return ObjectMsgPtr<VmInstrChain>::NewFrom(mut_allocator(), vm_instr_msg, this);
  }
  ObjectMsgPtr<VmInstrChain> vm_instr_chain = mut_free_chain_list()->PopFront();
  vm_instr_chain->__Init__(vm_instr_msg, this);
  return vm_instr_chain;
}

void VmStream::DeleteVmInstrChain(ObjectMsgPtr<VmInstrChain>&& vm_instr_chain) {
  CHECK(vm_instr_chain->is_pending_chain_link_empty());
  CHECK_EQ(vm_instr_chain->ref_cnt(), 1);
  mut_free_chain_list()->EmplaceBack(std::move(vm_instr_chain));
  vm_instr_chain->__Delete__();
}

}  // namespace oneflow
