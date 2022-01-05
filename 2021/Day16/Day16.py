from math import prod

class Packet:
    def __init__(self, data, mode = 'hex') -> None:
        self.__parse(data, mode)
        
    def __parse(self, data, mode):
        if mode == 'hex':
            self.binary = bin(int(data, 16))[2:].zfill(4 * len(data))
        elif mode == 'bin':
            self.binary = data
        else:
            raise Exception
            
        self.version = int(self.binary[:3], 2)
        self.type_id = int(self.binary[3:6], 2)

        if self.type_id == 4: # literal value
            self.type = 'value'
            self.binary = self.binary[:6] + self.__parse_literal_value(self.binary[6:])
        else: #operator
            self.type = 'operator'
            self.binary = self.binary[:6] + self.__parse_operator(self.binary[6:])
        pass

    def __parse_literal_value(self, binary):
        result = ''
        for i in range(int(len(binary)/5)):
            prefix = binary[i * 5:i * 5 + 1]
            result += binary[i * 5 + 1:i * 5 + 5]
            if prefix == '0':
                i_break = i
                break
        self.value = int(result, 2)
        return binary[:i_break * 5 + 5] # return binary part that was actually used
        
    def __parse_operator(self, binary):
        self.sub_packets = []
        self.length_type_id = binary[:1]
        if self.length_type_id == '0': # next 15 bits represent total length in bits
            length_in_bits = int(binary[1:16], 2)
            return binary[:16] + self.__parse_sub_packets(binary[16:16+length_in_bits])
        elif self.length_type_id == '1': # next 11 bits are number of sub-packets immediately contained
            no_of_sub_packets = int(binary[1:12], 2)
            return binary[:12] + self.__parse_sub_packets(binary[12:], no_of_sub_packets)
        else:
            raise Exception

    def __parse_sub_packets(self, binary, no_of_sub_packets = -1):
        result = binary
        
        while len(binary) > 0 and (no_of_sub_packets == -1 or (no_of_sub_packets != -1 and len(self.sub_packets) != no_of_sub_packets)):
            if binary.count('0') == len(binary):
                break
            sub_packet = Packet(binary, mode='bin')
            self.sub_packets.append(sub_packet)
            binary = binary[len(sub_packet.binary):]
        
        # if len(binary) > 0:
        #     assert binary.count('0') == len(binary)

        return result[:-len(binary) if len(binary) > 0 else len(result)]
            
    @property
    def version_sum(self):
        sub_packets_sum = 0
        if self.type == 'operator':
            for sub_packet in self.sub_packets:
                sub_packets_sum += sub_packet.version_sum
        return self.version + sub_packets_sum
    
    def getValue(self):
        if self.type == 'value':
            return self.value
        elif self.type == 'operator':
            match self.type_id:
                case 0: # sum
                    return sum(map(lambda x: x.getValue(), self.sub_packets))
                case 1: # product
                    return prod(map(lambda x: x.getValue(), self.sub_packets))
                case 2: # minimum
                    return min(self.sub_packets, key=lambda x: x.getValue()).getValue()
                case 3: # maximum
                    return max(self.sub_packets, key=lambda x: x.getValue()).getValue()
                case 5: # greater than
                    assert len(self.sub_packets) == 2
                    return 1 if self.sub_packets[0].getValue() > self.sub_packets[1].getValue() else 0
                case 6: # less than
                    assert len(self.sub_packets) == 2
                    return 1 if self.sub_packets[0].getValue() < self.sub_packets[1].getValue() else 0
                case 7: # equal to
                    assert len(self.sub_packets) == 2
                    return 1 if self.sub_packets[0].getValue() == self.sub_packets[1].getValue() else 0
                case _:
                    raise Exception
        else:
           raise Exception 
       
    def debug(self):
        if self.type == 'value':
            return str(self.value)
        s = ''
        if self.type == 'operator':
            match self.type_id:
                case 0:
                    s += 'sum'
                case 1:
                    s += 'prod'
                case 2:
                    s += 'min'
                case 3:
                    s += 'max'
                case 5:
                    s += 'gt'
                case 6:
                    s += 'lt'
                case 7:
                    s += 'eq'
                case _:
                    raise Exception
        s += '('
        for i in range(len(self.sub_packets)):
            s += self.sub_packets[i].debug()
            if i != len(self.sub_packets) - 1:
                s += ', '
        s += ')'
        return s
    
def parse(file):
    with open(file, 'r') as f:
        return f.readline()

def main():
    hex = parse('input.txt')
    
    packet = Packet('D2FE28')
    assert packet.type == 'value'
    assert packet.value == 2021
    assert packet.binary == '110100101111111000101'
    
    packet = Packet('38006F45291200')
    assert packet.type == 'operator'
    assert len(packet.sub_packets) == 2
    assert packet.sub_packets[0].value == 10
    assert packet.sub_packets[1].value == 20
    
    packet = Packet('EE00D40C823060')
    assert packet.type == 'operator'
    assert len(packet.sub_packets) == 3
    assert packet.sub_packets[0].value == 1
    assert packet.sub_packets[1].value == 2
    assert packet.sub_packets[2].value == 3
    
    packet = Packet('8A004A801A8002F478')
    assert packet.version_sum == 16
    
    packet = Packet('620080001611562C8802118E34')
    assert packet.version_sum == 12
    
    packet = Packet('C0015000016115A2E0802F182340')
    assert packet.version_sum == 23
    
    packet = Packet('A0016C880162017C3686B18A3D4780')
    assert packet.version_sum == 31
    
    inputPacket = Packet(hex)
    print(f'Pt1: {inputPacket.version_sum}')
    
    packet = Packet('C200B40A82')
    assert packet.getValue() == 3
    
    packet = Packet('04005AC33890')
    assert packet.getValue() == 54
    
    packet = Packet('880086C3E88112')
    assert packet.getValue() == 7

    packet = Packet('CE00C43D881120')
    assert packet.getValue() == 9
    
    packet = Packet('D8005AC2A8F0')
    assert packet.getValue() == 1

    packet = Packet('F600BC2D8F')
    assert packet.getValue() == 0
    
    packet = Packet('9C005AC2F8F0')
    assert packet.getValue() == 0
    
    packet = Packet('9C0141080250320F1802104A08')
    assert packet.getValue() == 1
    
    print(f'Pt2: {inputPacket.getValue()}')

if __name__ == '__main__':
    main()
