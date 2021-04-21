
class Controller:
    def __init__(self, odom, hlc, start_time):
        self.odom = odom
        self.hlc = hlc
        self.current_hlc_index = 0
        self.start_time = start_time
        self.time = []

        self.setup_controller()

    def setup_controller(self):
        self.kp_n = 1.2
        self.kd_n = 0.4
        self.ki_n = 0.3
        self.kd_e = 1.2
        self.kp_e = 0.4
        self.ki_e = 0.3
        self.kp_d = 1.0
        self.kd_d = 0.8
        self.ki_d = 0.0

        self.kp_u = 0.5
        self.kd_u = 0.13
        self.ki_u = 0.0
        self.kp_v = 0.5
        self.kd_v = 0.13
        self.ki_v = 0.0
        self.kp_w = 0.6
        self.kd_w = 0.1
        self.ki_w = 0.25

        self.maxNDot = 3.0
        self.maxEDot = 3.0
        self.maxDDot = 0.5

        self.nPID = PIDController(self.kp_n,self.kd_n,self.ki_n,self.maxNDot)
        self.ePID = PIDController(self.kp_e,self.kd_e,self.ki_e,self.maxEDot)
        self.dPID = PIDController(self.kp_d,self.kd_d,self.ki_d,self.maxDDot)
        # self.uPID = PIDController(self.kp_u,self.kd_u,self.ki_u)
        # self.vPID = PIDController(self.kp_v,self.kd_v,self.ki_v)
        # self.wPID = PIDController(self.kp_w,self.kd_w,self.ki_w)

    def run_controller(self):
        for i in range(len(self.odom.time)):
            if self.odom.time[i] >= self.start_time:
                self.time.append(self.odom.time[i])
                if i == 0:
                    dt = 0.1
                else:
                    dt = self.time[-1] - self.odom.time[i-1]
                self.update_hlc_index(self.time[-1])
                self.nPID.update_control(self.odom.position[0][i],self.hlc.position[0][self.current_hlc_index],dt)
                self.ePID.update_control(self.odom.position[1][i],self.hlc.position[1][self.current_hlc_index],dt)
                self.dPID.update_control(self.odom.position[2][i],self.hlc.position[2][self.current_hlc_index],dt)
                # self.uPID.update_control(self.odom.velocity[0][i],self.nPID.command[-1],dt)
                # self.vPID.update_control(self.odom.velocity[1][i],self.ePID.command[-1],dt)
                # self.wPID.update_control(self.odom.velocity[2][i],self.dPID.command[-1],dt)

    def update_hlc_index(self,time):
        if time < self.hlc.time[-1]:
            while self.hlc.time[self.current_hlc_index+1] <= time:
                self.current_hlc_index = self.current_hlc_index + 1

class PIDController:
    def __init__(self,kp,kd,ki,max):
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.max = max
        self.min = -max

        self.integrator = []
        self.xDot = 0.0
        self.prevX = 0.0
        self.prevError = 0.0
        self.tau = 0.05

        self.command = []

    def update_control(self,x,xc,dt):
        error = xc-x
        self.update_xDot(x,dt)
        self.update_integrator(error,dt)

        kTerm = self.kp*error
        dTerm = self.kd*self.xDot
        iTerm = self.ki*self.integrator[-1]
        u = kTerm-dTerm+iTerm
        self.command.append(self.compute_anti_windup(u,kTerm,dTerm,iTerm))

        self.prevX = x

    def update_xDot(self,x,dt):
        self.xDot = (2.0*self.tau - dt)/(2.0*self.tau + dt)*self.xDot + 2.0/(2.0*self.tau + dt)*(x-self.prevX)

    def update_integrator(self,error,dt):
        if not self.integrator:
            self.integrator.append(dt / 2.0 * (error + self.prevError))
        else:
            self.integrator.append(self.integrator[-1] + dt/2.0*(error + self.prevError))

    def compute_anti_windup(self,u,p_term,d_term,i_term):
        u_sat = self.saturate(u)
        if u != u_sat and abs(i_term) > abs(u_sat - p_term + d_term):
          self.integrator[-1] = (u_sat - p_term + d_term)/self.ki
        return u_sat


    def saturate(self, u):
        if u>self.max:
            return self.max
        if u<self.min:
            return self.min
        else:
            return u


