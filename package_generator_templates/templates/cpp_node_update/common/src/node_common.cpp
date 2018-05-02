/**
* @file {nodeName}_common.cpp
* @author {packageAuthor}
*
* Copyright (C) {packageCopyright}
*
* @brief {packageDescription}
*        This file is to be edited by the Developer
**/

// ROS message includes
#include "ros/ros.h"

// ROS message & services includes

{ifactionServer}
#include <actionlib/server/simple_action_server.h>
{forallactionServer}
#include <{apply-get_cpp_path}Action.h>
{endforallactionServer}
{endifactionServer}
{ifactionClient}
#include <actionlib/client/simple_action_client.h>
{forallactionClient}
#include <{apply-get_cpp_path}Action.h>
{endforallactionClient}
{endifactionClient}
{ifdynParam}
#include <dynamic_reconfigure/server.h>
#include <{packageName}/{nodeName}Config.h>

{endifdynParam}
// ROS message & services includes
{forallpublisher}
#include <{apply-get_cpp_path}.h>
{endforallpublisher}
{foralldirectpublisher}
#include <{apply-get_cpp_path}.h>
{endforalldirectpublisher}
{forallsubscriber}
#include <{apply-get_cpp_path}.h>
{endforallsubscriber}
{foralldirectsubscriber}
#include <{apply-get_cpp_path}.h>
{endforalldirectsubscriber}
{forallserviceServer}
#include <{apply-get_cpp_path}.h>
{endforallserviceServer}
{forallserviceClient}
#include <{apply-get_cpp_path}.h>
{endforallserviceClient}

{iflistener}
#include <tf/transform_listener.h>
{endiflistener}
{ifbroadcaster}
#include <tf/transform_broadcaster.h>
{endifbroadcaster}

/* protected region user include files begin */
/* protected region user include files end */

/**
 * @class {camelCaseNodeName}Config
 * @brief set of static and dynamic parameters
 * @warning this class is autogenerated. It should not be touched!
 */
class {camelCaseNodeName}Config
{
public:
    {ifparam}
    // parameters handled through the parameter server
    {endifparam}
    {forallparam}
    {type} {name};
    {endforallparam}
    {ifdynParam}
    // dynamic parameters handled through dynamic reconfigure
    {endifdynParam}
    {foralldynParam}
    {type} {name};
    {endforalldynParam}
};

/**
 * @class {camelCaseNodeName}Data
 * @brief set of input / output handled through the update methods
 * @warning this class is autogenerated. It should not be touched!
 */
class {camelCaseNodeName}Data
{
public:
    {ifsubscriber}
    //input data
    {endifsubscriber}
    {forallsubscriber}
    {type} in_{name};
    bool in_{name}_updated;
    {endforallsubscriber}
    {ifpublisher}
    //output data
    {endifpublisher}
    {forallpublisher}
    {type} out_{name};
    bool out_{name}_active;
    {endforallpublisher}
};

/**
 * @class {camelCaseNodeName}Passthrough
 * @brief set of passthrough elements slightly violating interface / implementation separation
 * @warning this class is autogenerated. It should not be touched!
 */
class {camelCaseNodeName}Passthrough
{
public:
    {foralllistener}
    tf::TransformListener {name};
    {endforalllistener}
    {forallbroadcaster}
    tf::TransformBroadcaster {name};
    {endforallbroadcaster}
    {foralldirectpublisher}
    ros::Publisher {name};
    {endforalldirectpublisher}
    {foralldirectsubscriber}
    ros::Subscriber {name};
    {endforalldirectsubscriber}

    {forallserviceClient}
    ros::ServiceClient client_{name};
    {endforallserviceClient}
    {forallactionClient}
    actionlib::SimpleActionClient<{type}Action> * ac_{name};
    {endforallactionClient}

    /**
     * @brief constructor
     */
    {camelCaseNodeName}Passthrough()
    {
        {forallactionClient}
        ac_{name} = NULL;
        {endforallactionClient}
    }
    /**
     * @brief destructor
     */
    ~{camelCaseNodeName}Passthrough()
    {
        {forallactionClient}
        delete ac_{name};
        {endforallactionClient}
    }
};
/**
 * @class {camelCaseNodeName}Impl
 * @brief Implementation of the node intelligence
 * @warning this class is be filled by the Developer, at locations indicated
 */
class {camelCaseNodeName}Impl
{
    /* protected region user member variables begin */
    /* protected region user member variables end */

public:
    {camelCaseNodeName}Passthrough passthrough;

    /**
     * @brief constructor
     */
    {camelCaseNodeName}Impl()
    {
        /* protected region user constructor begin */
        /* protected region user constructor end */
    }
    /**
     * @brief destructor
     */
    ~{camelCaseNodeName}Impl()
    {
        /* protected region user destructor begin */
        /* protected region user destructor end */
    }
    /**
     * @brief method called at node configuration
     * @param config set of configuration parameters available
     */
    void configure({camelCaseNodeName}Config config)
    {
        /* protected region user configure begin */
        /* protected region user configure end */
    }
    /**
     * @brief Update method periodically called by the ros component
     * @param data contains received messages (through subscription), and will contain messages to publish
     * @param config latest state of the config variables
     */
    void update({camelCaseNodeName}Data &data, {camelCaseNodeName}Config config)
    {
        /* protected region user update begin */
        /* protected region user update end */
    }

    {forallactionServer}
    /**
     * @brief callback of an action request
     * @param goal objective provided by the caller
     * @param as_ handler of the action
     */
    void callback_{name}(const {type}GoalConstPtr &goal, actionlib::SimpleActionServer<{type}Action> *as_)
    {
        /* protected region user implementation of action callback for {name} begin */
        /* protected region user implementation of action callback for {name} end */
    }
    {endforallactionServer}
    {forallserviceServer}
    /**
     * @brief callback of a service request
     * @param req input parameters provided by the caller
     * @param res output parameters resulting from the service execution
     * @param config latest state of the config variables
     * @param as_ handler of the action
     */
    bool callback_{name}({type}::Request  &req, {type}::Response &res , {camelCaseNodeName}Config config)
    {
        /* protected region user implementation of service callback for {name} begin */
        /* protected region user implementation of service callback for {name} end */
        // todo remove that return
        return true;
    }
    {endforallserviceServer}
    {foralldirectsubscriber}
    /**
     * @brief direct callback of a topic subscription
     * @param msg message received on the topic
     * @warning this subscription is not driven through the update mechanism
     */
    void directTopicCallback_{name}(const {type}::ConstPtr& msg)
    {
        /* protected region user implementation of direct subscriber callback for {name} begin */
        /* protected region user implementation of direct subscriber callback for {name} end */
    }
    {endforalldirectsubscriber}
    /* protected region user additional functions begin */
    /* protected region user additional functions end */
};