from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub
import time


class NetworkMonitor(app_manager.RyuApp):
    # Use OpenFlow 1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(NetworkMonitor, self).__init__(*args, **kwargs)

        # Dictionary to store MAC learning table
        self.mac_to_port = {}

        # Store connected datapaths (switches)
        self.datapaths = {}

        # Store previous port statistics for bandwidth calculation
        self.port_stats = {}

        # Start monitoring thread
        self.monitor_thread = hub.spawn(self._monitor)

    # Triggered when switch connects to controller
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        ofproto = dp.ofproto
        parser = dp.ofproto_parser

        # Match all packets by default
        match = parser.OFPMatch()

        # Send unmatched packets to controller
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER)]

        # Install default rule
        self.add_flow(dp, 0, match, actions)

    # Helper function to add flow rules
    def add_flow(self, dp, priority, match, actions):
        parser = dp.ofproto_parser
        ofproto = dp.ofproto

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=dp,
            priority=priority,
            match=match,
            instructions=inst)

        dp.send_msg(mod)

    # Handle PacketIn messages from switch
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofproto = dp.ofproto
        parser = dp.ofproto_parser

        # Save datapath for monitoring
        dpid = dp.id
        self.datapaths[dpid] = dp

        in_port = msg.match['in_port']

        # Flood packets to all ports
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]

        out = parser.OFPPacketOut(
            datapath=dp,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=msg.data)

        dp.send_msg(out)

    # Background monitoring thread
    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self.request_stats(dp)

            # Poll every 2 seconds
            hub.sleep(2)

    # Send port statistics request to switch
    def request_stats(self, dp):
        parser = dp.ofproto_parser

        req = parser.OFPPortStatsRequest(
            dp, 0, dp.ofproto.OFPP_ANY)

        dp.send_msg(req)

    # Handle statistics reply from switch
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        body = ev.msg.body
        dpid = ev.msg.datapath.id

        for stat in body:
            port_no = stat.port_no
            tx_bytes = stat.tx_bytes
            rx_bytes = stat.rx_bytes

            key = (dpid, port_no)

            # If previous stats exist, calculate bandwidth
            if key in self.port_stats:
                old_tx, old_rx, old_time = self.port_stats[key]

                now = time.time()
                interval = now - old_time

                # Convert byte difference to Mbps
                tx_rate = (tx_bytes - old_tx) * 8 / interval / 1e6
                rx_rate = (rx_bytes - old_rx) * 8 / interval / 1e6

                print(
                    f"Switch {dpid} Port {port_no}: "
                    f"TX={tx_rate:.2f} Mbps "
                    f"RX={rx_rate:.2f} Mbps"
                )

            # Save current stats for next calculation
            self.port_stats[key] = (
                tx_bytes,
                rx_bytes,
                time.time()
            )