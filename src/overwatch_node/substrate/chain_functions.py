from typing import Any, Optional
from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt
from substrateinterface.exceptions import SubstrateRequestException
from tenacity import retry, stop_after_attempt, wait_exponential, wait_fixed
from substrate.config import BLOCK_SECS
from tenacity import RetryCallState

retry_counter = 0

def increment_counter(retry_state: RetryCallState):
    global retry_counter
    retry_counter += 1
    print(f"Retry {retry_counter}: {retry_state}")

def get_block_number(substrate: SubstrateInterface):
  @retry(wait=wait_fixed(BLOCK_SECS+1), stop=stop_after_attempt(4))
  def make_query():
    try:
      with substrate as _substrate:
        block_hash = _substrate.get_block_hash()
        block_number = _substrate.get_block_number(block_hash)
        return block_number
    except SubstrateRequestException as e:
      print("Failed to get query request: {}".format(e))

  return make_query()

def register_overwatch_node(
  substrate: SubstrateInterface,
  keypair: Keypair,
  hotkey: str,
  peer_id: str,
  stake_to_be_added: int,
  a: Optional[str] = None,
  b: Optional[str] = None,
  c: Optional[str] = None,
) -> ExtrinsicReceipt:
  """
  Add subnet validator as subnet subnet_node to blockchain storage

  :param substrate: interface to blockchain
  :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
  """

  # compose call
  call = substrate.compose_call(
    call_module='Network',
    call_function='register_overwatch_node',
    call_params={
      'hotkey': hotkey,
      'peer_id': peer_id,
      'stake_to_be_added': stake_to_be_added,
      'a': a,
      'b': b,
      'c': c,
    }
  )

  @retry(wait=wait_fixed(BLOCK_SECS+1), stop=stop_after_attempt(4))
  def submit_extrinsic():
    try:
      with substrate as _substrate:
        # get none on retries
        nonce = _substrate.get_account_nonce(keypair.ss58_address)

        # create signed extrinsic
        extrinsic = _substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=nonce)

        receipt = _substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt
    except SubstrateRequestException as e:
      print("Failed to send: {}".format(e))

  return submit_extrinsic()

def activate_overwatch_node(
  substrate: SubstrateInterface,
  keypair: Keypair,
  overwatch_node_id: int,
) -> ExtrinsicReceipt:
  """
  Add subnet validator as subnet subnet_node to blockchain storage

  :param substrate: interface to blockchain
  :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
  """

  # compose call
  call = substrate.compose_call(
    call_module='Network',
    call_function='activate_overwatch_node',
    call_params={
      'overwatch_node_id': overwatch_node_id,
    }
  )

  @retry(wait=wait_fixed(BLOCK_SECS+1), stop=stop_after_attempt(4))
  def submit_extrinsic():
    try:
      with substrate as _substrate:
        # get none on retries
        nonce = _substrate.get_account_nonce(keypair.ss58_address)

        # create signed extrinsic
        extrinsic = _substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=nonce)

        receipt = _substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt
    except SubstrateRequestException as e:
      print("Failed to send: {}".format(e))

  return submit_extrinsic()

def add_to_stake(
  substrate: SubstrateInterface,
  keypair: Keypair,
  stake_to_be_added: int,
):
  """
  Add subnet validator as subnet subnet_node to blockchain storage

  :param substrate: interface to blockchain
  :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
  :param stake_to_be_added: stake to be added towards subnet
  """

  # compose call
  call = substrate.compose_call(
    call_module='Network',
    call_function='add_to_overwatch_stake',
    call_params={
      'stake_to_be_added': stake_to_be_added,
    }
  )

  @retry(wait=wait_fixed(BLOCK_SECS+1), stop=stop_after_attempt(4))
  def submit_extrinsic():
    try:
      with substrate as _substrate:
        # get none on retries
        nonce = _substrate.get_account_nonce(keypair.ss58_address)

        # create signed extrinsic
        extrinsic = _substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=nonce)

        receipt = _substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt
    except SubstrateRequestException as e:
      print("Failed to send: {}".format(e))

  return submit_extrinsic()

def remove_stake(
  substrate: SubstrateInterface,
  keypair: Keypair,
  stake_to_be_removed: int,
):
  """
  Remove stake balance towards specified subnet

  Amount must be less than allowed amount that won't allow stake balance to be lower than
  the required minimum balance

  :param substrate: interface to blockchain
  :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
  :param stake_to_be_removed: stake to be removed from subnet
  """

  # compose call
  call = substrate.compose_call(
    call_module='Network',
    call_function='remove_overwatch_stake',
    call_params={
      'stake_to_be_removed': stake_to_be_removed,
    }
  )

  @retry(wait=wait_fixed(BLOCK_SECS+1), stop=stop_after_attempt(4))
  def submit_extrinsic():
    try:
      with substrate as _substrate:
        # get none on retries
        nonce = _substrate.get_account_nonce(keypair.ss58_address)

        # create signed extrinsic
        extrinsic = _substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=nonce)

        receipt = _substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt
    except SubstrateRequestException as e:
      print("Failed to send: {}".format(e))

  return submit_extrinsic()

def submit_benchmark_weights(
  substrate: SubstrateInterface,
  keypair: Keypair,
  encrypted_weights,
):
  """
  Submit consensus data on each epoch with no conditionals

  It is up to prior functions to decide whether to call this function

  :param substrate: interface to blockchain
  :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
  :param consensus_data: an array of data containing all AccountIds, PeerIds, and scores per subnet hoster

  Note: It's important before calling this to ensure the entrinsic will be successful.
        If the function reverts, the extrinsic is Pays::Yes
  """
  # compose call
  call = substrate.compose_call(
    call_module='Network',
    call_function='submit_benchmark_weights',
    call_params={
      'encrypted_weights': encrypted_weights,
    }
  )

  # @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(4), after=increment_counter)
  @retry(wait=wait_fixed(BLOCK_SECS+1), stop=stop_after_attempt(4), after=increment_counter)
  def submit_extrinsic():
    try:
      with substrate as _substrate:
        # get none on retries
        nonce = _substrate.get_account_nonce(keypair.ss58_address)

        # create signed extrinsic
        extrinsic = _substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=nonce)

        receipt = _substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        if receipt.is_success:
          print('✅ Success, triggered events:')
          for event in receipt.triggered_events:
              print(f'* {event.value}')
        else:
            print('⚠️ Extrinsic Failed: ', receipt.error_message)

        return receipt
    except SubstrateRequestException as e:
      print("Failed to send: {}".format(e))

  return submit_extrinsic()