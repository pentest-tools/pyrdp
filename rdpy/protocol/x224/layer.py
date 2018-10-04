from rdpy.core import log
from rdpy.core.newlayer import Layer
from rdpy.core.subject import Subject
from pdu import X224Parser, X224Data, X224Header, X224ConnectionRequest, X224ConnectionConfirm, X224DisconnectRequest

class X224Observer:
    def connectionRequest(self, pdu):
        raise Exception("Unhandled X224 Connection Request PDU")

    def connectionConfirm(self, pdu):
        raise Exception("Unhandled X224 Connection Confirm PDU")
    
    def disconnectRequest(self, pdu):
        raise Exception("Unhandled X224 Disconnect Request PDU")
    
    def error(self, pdu):
        raise Exception("Unhandled X224 Error PDU")

class X224Layer(Layer, Subject):
    """
    @summary: Layer for handling X224 related traffic
    """

    def __init__(self):
        super(X224Layer, self).__init__()
        super(X224Layer, self).__init__()
        self.parser = X224Parser()
    
    def setObserver(self, observer):
        super(X224Layer, self).setObserver(observer)
        self.handlers = {
            X224Header.X224_TPDU_CONNECTION_REQUEST: self.observer.connectionRequest,
            X224Header.X224_TPDU_CONNECTION_CONFIRM: self.observer.connectionConfirm,
            X224Header.X224_TPDU_DISCONNECT_REQUEST: self.observer.disconnectRequest,
            X224Header.X224_TPDU_ERROR: self.observer.error
        }
    
    def recv(self, data):
        pdu = self.parser.parse(data)

        if pdu.header == X224Header.X224_TPDU_DATA:
            self.next.recv(pdu.payload)
        elif pdu.header in self.handlers:
            self.handlers[pdu.header](pdu)
        else:
            raise Exception("Unhandled PDU received")
    
    def send(self, payload, **kwargs):
        roa = kwargs.pop("roa", False)
        eot = kwargs.pop("eot", True)
        
        pdu = X224Data(roa, eot, payload)
        self.previous.send(self.parser.write(pdu))
    
    def sendConnectionPDU(self, factory, payload, **kwargs):
        credit = kwargs.pop("credit", 0)
        destination = kwargs.pop("destination", 0)
        source = kwargs.pop("source", 0)
        options = kwargs.pop("options", 0)

        pdu = factory(credit, destination, source, options, payload)
        self.previous.send(self.parser.write(pdu))

    def sendConnectionRequest(self, payload, **kwargs):
        self.sendConnectionPDU(X224ConnectionRequest, payload, **kwargs)
    
    def sendConnectionConfirm(self, payload, **kwargs):
        self.sendConnectionPDU(X224ConnectionConfirm, payload, **kwargs)
    
    def sendDisconnectRequest(self, reason, **kwargs):
        destination = kwargs.pop("destination", 0)
        source = kwargs.pop("source", 0)
        payload = kwargs.pop("payload", "")

        pdu = X224DisconnectRequest(destination, source, reason, payload)
        self.previous.send(self.parser.write(pdu))
    
    def sendError(self, cause, **kwargs):
        destination = kwargs.pop("destination", 0)

        pdu = X224Error(destination, cause)
        self.previous.send(self.parser.write(pdu))